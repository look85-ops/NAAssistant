Param(
  [Parameter(Mandatory=$true)][string]$Path,
  [Parameter(Mandatory=$true)][string]$Out,
  [string]$KeywordsFile = "docs/aos/keywords/topics_ru.txt"
)

# Offline comment bucketing by keywords (no external APIs), semicolon CSV, last column is comment

if (-not (Test-Path -LiteralPath $Path)) { Write-Error "Path not found"; exit 1 }

$files = if (Test-Path -LiteralPath $Path -PathType Leaf) { ,(Get-Item -LiteralPath $Path) } else { Get-ChildItem -LiteralPath $Path -Filter *.csv -File | Sort-Object Name }
if (-not $files -or $files.Count -eq 0) { Write-Error "No CSV files"; exit 1 }

# Load topics
$topicRules = @()
if (Test-Path -LiteralPath $KeywordsFile) {
  $lines = Get-Content -LiteralPath $KeywordsFile -Encoding UTF8 | Where-Object { $_ -and -not $_.StartsWith('#') }
  foreach ($ln in $lines) {
    $parts = $ln.Split(':',2)
    if ($parts.Count -lt 2) { continue }
    $name = $parts[0].Trim()
    $keys = $parts[1].Split(',') | ForEach-Object { $_.Trim().ToLowerInvariant() } | Where-Object { $_ }
    if ($name -and $keys.Count -gt 0) { $topicRules += [pscustomobject]@{Name=$name; Keys=$keys} }
  }
}
if ($topicRules.Count -eq 0) { Write-Error "No topics loaded"; exit 1 }

$buckets = @{}
function Add-Bucket($n){ if (-not $buckets.ContainsKey($n)) { $buckets[$n] = @() } }
foreach ($tr in $topicRules) { Add-Bucket $tr.Name }
Add-Bucket 'Other'

foreach ($file in $files) {
  $lines = Get-Content -LiteralPath $file.FullName -Encoding UTF8
  if (-not $lines) { continue }
  $isHeader = $true
  foreach ($ln in $lines) {
    if ($isHeader) { $isHeader = $false; continue }
    if ([string]::IsNullOrWhiteSpace($ln)) { continue }
    $parts = $ln -split ';'
    if ($parts.Length -lt 14) { continue }
    $comment = $parts[-1].Trim()
    if ([string]::IsNullOrWhiteSpace($comment)) { continue }
    $lc = $comment.ToLowerInvariant()
    $placed = $false
    foreach ($tr in $topicRules) {
      foreach ($k in $tr.Keys) {
        if ($lc.Contains($k)) { $buckets[$tr.Name] += $comment; $placed = $true; break }
      }
      if ($placed) { break }
    }
    if (-not $placed) { $buckets['Other'] += $comment }
  }
}

$outLines = @('# AOS Comments: Local Topics (draft)','')
foreach ($k in ($buckets.Keys | Sort-Object)) {
  $outLines += ("## {0} ({1})" -f $k, $buckets[$k].Count)
  $outLines += ''
  $outLines += ($buckets[$k] | Select-Object -First 5 | ForEach-Object { '- ' + $_ })
  $outLines += ''
}

$outPath = [System.IO.Path]::GetFullPath($Out)
$outDir = Split-Path -Parent $outPath
if (-not (Test-Path -LiteralPath $outDir)) { New-Item -ItemType Directory -Path $outDir -Force | Out-Null }
$outLines -join "`n" | Out-File -LiteralPath $outPath -Encoding UTF8
Write-Output ("Wrote {0}" -f $outPath)

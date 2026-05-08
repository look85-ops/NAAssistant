Param(
  [Parameter(Mandatory=$true)][string]$Path,
  [Parameter(Mandatory=$true)][string]$Out
)

# Local-only comment classifier: extracts the last text column and groups simple topics by keywords
# No external API calls. Works offline.

$files = Get-ChildItem -LiteralPath $Path -Filter *.csv -File | Sort-Object Name
if (-not $files -or $files.Count -eq 0) { Write-Error "No CSV files"; exit 1 }

$topics = @{}
function Add-Topic($name) { if (-not $topics.ContainsKey($name)) { $topics[$name] = @() } }

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
    $bucket = 'Other'
    if ($lc -match 'эконом') { $bucket = 'Economics/ROI' }
    elseif ($lc -match 'инновац|нов|nk|нк') { $bucket = 'Innovation/NDT/maintenance' }
    elseif ($lc -match 'выезд|полев|предприяти') { $bucket = 'Field day/onsite' }
    elseif ($lc -match 'практик|пример|кейс') { $bucket = 'Practice/examples' }
    elseif ($lc -match 'интерес') { $bucket = 'Interest' }
    elseif ($lc -match 'общен|дискус') { $bucket = 'Discussion/interaction' }
    Add-Topic $bucket
    $topics[$bucket] += $comment
  }
}

$outLines = @('# AOS Comments: Local Topics (draft)','')
foreach ($k in ($topics.Keys | Sort-Object)) {
  $outLines += ("## {0} ({1})" -f $k, $topics[$k].Count)
  $outLines += ''
  $outLines += ($topics[$k] | Select-Object -First 5 | ForEach-Object { '- ' + $_ })
  $outLines += ''
}

$outPath = [System.IO.Path]::GetFullPath($Out)
$outDir = Split-Path -Parent $outPath
if (-not (Test-Path -LiteralPath $outDir)) { New-Item -ItemType Directory -Path $outDir -Force | Out-Null }
$outLines -join "`n" | Out-File -LiteralPath $outPath -Encoding UTF8
Write-Output ("Wrote {0}" -f $outPath)

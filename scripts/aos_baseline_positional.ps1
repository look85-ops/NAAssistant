Param(
  [Parameter(Mandatory=$true)][string]$Path,
  [Parameter(Mandatory=$true)][string]$Out
)

# Collect CSV files
if (Test-Path -LiteralPath $Path -PathType Leaf) {
  $files = ,(Get-Item -LiteralPath $Path)
} else {
  $files = Get-ChildItem -LiteralPath $Path -Filter *.csv -File | Sort-Object Name
}
if (-not $files -or $files.Count -eq 0) {
  Write-Error "No CSV files found at $Path"
  exit 1
}

# Metric indices (0-based): columns 9..13 in the CSV
$metricIdx = 8..12
$metricNames = @('Clarity','Engagement','Answers','Interest','Practicality')

function Parse-Number([string]$s) {
  if ([string]::IsNullOrWhiteSpace($s)) { return $null }
  $x = $s.Trim().Replace(',', '.')
  $d = $null
  if ([double]::TryParse($x, [System.Globalization.NumberStyles]::Any, [System.Globalization.CultureInfo]::InvariantCulture, [ref]$d)) {
    return $d
  }
  return $null
}

$overall = @{}
$perFile = @()
$totalRows = 0

foreach ($file in $files) {
  $acc = @{}
  foreach ($i in 0..($metricNames.Count-1)) { $acc[$i] = @() }

  $lines = Get-Content -LiteralPath $file.FullName -Encoding UTF8
  if (-not $lines) { continue }
  $isHeader = $true
  foreach ($ln in $lines) {
    if ($isHeader) { $isHeader = $false; continue }
    if ([string]::IsNullOrWhiteSpace($ln)) { continue }
    $parts = $ln -split ';'
    if ($parts.Length -lt 13) { continue }
    $totalRows += 1
    for ($k=0; $k -lt $metricIdx.Count; $k++) {
      $idx = $metricIdx[$k]
      if ($idx -lt $parts.Length) {
        $v = Parse-Number($parts[$idx])
        if ($v -ne $null) { $acc[$k] += $v }
      }
    }
  }

  foreach ($k in 0..($metricNames.Count-1)) {
    if (-not $overall.ContainsKey($k)) { $overall[$k] = @() }
    $overall[$k] += $acc[$k]
  }

  $avgs = @{}
  foreach ($k in 0..($metricNames.Count-1)) {
    $vals = $acc[$k]
    if ($vals.Count -gt 0) { $avgs[$k] = ($vals | Measure-Object -Average).Average } else { $avgs[$k] = $null }
  }
  $perFile += [pscustomobject]@{ Name=$file.Name; Rows=($lines.Count-1); Avgs=$avgs }
}

$overallAvg = @{}
foreach ($k in 0..($metricNames.Count-1)) {
  $vals = $overall[$k]
  if ($vals -and $vals.Count -gt 0) { $overallAvg[$k] = ($vals | Measure-Object -Average).Average } else { $overallAvg[$k] = $null }
}

function Fmt([double]$x) { if ($null -eq $x) { return '—' } else { return ('{0:N2}' -f $x) } }

$outLines = @()
$outLines += '# AOS Baseline (draft)'
$outLines += ''
$outLines += ('Files: {0}; Rows: ~{1}' -f $files.Count, $totalRows)
$outLines += ''
$outLines += '## Overall averages'
for ($k=0; $k -lt $metricNames.Count; $k++) {
  $outLines += ('- {0}: {1}' -f $metricNames[$k], (Fmt $overallAvg[$k]))
}
$outLines += ''
$outLines += '## By file'
foreach ($pf in $perFile) {
  $outLines += ('### {0} (rows: ~{1})' -f $pf.Name, $pf.Rows)
  for ($k=0; $k -lt $metricNames.Count; $k++) {
    $outLines += ('- {0}: {1}' -f $metricNames[$k], (Fmt $pf.Avgs[$k]))
  }
  $outLines += ''
}

$outPath = [System.IO.Path]::GetFullPath($Out)
$outDir = Split-Path -Parent $outPath
if (-not (Test-Path -LiteralPath $outDir)) { New-Item -ItemType Directory -Path $outDir -Force | Out-Null }
$outLines -join "`n" | Out-File -LiteralPath $outPath -Encoding UTF8
Write-Output ("Wrote {0}" -f $outPath)

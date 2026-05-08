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

$metricNamesPreferred = @(
  'Преподаватель понятно излагает материал',
  'Во время обучения Вы чувствовали себя включенным в работу',
  'Преподаватель качественно и полно отвечает на вопросы участников',
  'Обучение было для меня интересным',
  'Знания и навыки, полученные в ходе обучения, имеют практическую применяемость'
)
$metricLastFallback = 'Знания и навыки, полученные в ходе обучения, имеют практическую применимость'

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
  $rows = Import-Csv -LiteralPath $file.FullName -Delimiter ';'
  if (-not $rows) { continue }
  $headers = @()
  if ($rows.Count -gt 0) { $headers = $rows[0].PsObject.Properties.Name }

  # Build actual metric header list for this file (handle fallback spelling)
  $metrics = @()
  foreach ($mn in $metricNamesPreferred) {
    if ($mn -eq $metricNamesPreferred[-1]) {
      if ($headers -contains $mn) { $metrics += $mn }
      elseif ($headers -contains $metricLastFallback) { $metrics += $metricLastFallback }
    } else {
      if ($headers -contains $mn) { $metrics += $mn }
    }
  }
  if ($metrics.Count -eq 0) { continue }

  $acc = @{}
  foreach ($m in $metrics) { $acc[$m] = @() }

  foreach ($r in $rows) {
    $totalRows += 1
    foreach ($m in $metrics) {
      $v = Parse-Number($r.$m)
      if ($v -ne $null) { $acc[$m] += $v }
    }
  }

  # Aggregate overall
  foreach ($m in $metrics) {
    if (-not $overall.ContainsKey($m)) { $overall[$m] = @() }
    $overall[$m] += $acc[$m]
  }

  # Compute averages per file
  $avgs = @{}
  foreach ($m in $metrics) {
    $vals = $acc[$m]
    if ($vals.Count -gt 0) {
      $avgs[$m] = ($vals | Measure-Object -Average).Average
    } else {
      $avgs[$m] = $null
    }
  }
  $perFile += [pscustomobject]@{ Name=$file.Name; Rows=$rows.Count; Avgs=$avgs }
}

# Overall averages
$overallAvg = @{}
foreach ($kv in $overall.GetEnumerator()) {
  $vals = $kv.Value
  if ($vals.Count -gt 0) {
    $overallAvg[$kv.Key] = ($vals | Measure-Object -Average).Average
  } else { $overallAvg[$kv.Key] = $null }
}

function Fmt([double]$x) { if ($null -eq $x) { return '—' } else { return ('{0:N2}' -f $x) } }

$lines = @()
$lines += '# Базовый замер AOS (черновой)'
$lines += ''
$lines += ('Файлов: {0}; Ответов (строк): ~{1}' -f $files.Count, $totalRows)
$lines += ''
$lines += '## Средние значения по всем файлам'
foreach ($k in ($overallAvg.Keys | Sort-Object)) {
  $lines += ('- {0}: {1}' -f $k, (Fmt $overallAvg[$k]))
}
$lines += ''
$lines += '## По файлам'
foreach ($pf in $perFile) {
  $lines += ('### {0} (строк: ~{1})' -f $pf.Name, $pf.Rows)
  foreach ($k in ($pf.Avgs.Keys | Sort-Object)) {
    $lines += ('- {0}: {1}' -f $k, (Fmt $pf.Avgs[$k]))
  }
  $lines += ''
}

$outPath = [System.IO.Path]::GetFullPath($Out)
$outDir = Split-Path -Parent $outPath
if (-not (Test-Path -LiteralPath $outDir)) { New-Item -ItemType Directory -Path $outDir -Force | Out-Null }
$lines -join "`n" | Out-File -LiteralPath $outPath -Encoding UTF8
Write-Output ("Wrote {0}" -f $outPath)

<#
ASCII-only PowerShell script to audit AGENTS.md and .opencode/agent/*.md
Finds verbosity indicators and repeated lines within and across files.
#>

param(
  [string[]]$Paths = @('.opencode/agent/*.md','AGENTS.md'),
  [string]$Output = ''
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Get-FileStats {
  param([string]$Path)
  $content = Get-Content -Path $Path -Raw
  $lines = $content -split "`r?`n"
  $trimmed = $lines | ForEach-Object { $_.TrimEnd() }

  $lineCount = $trimmed.Count
  $wordCount = (($content -split "\s+" | Where-Object { $_ -ne '' }).Count)
  $headings = ($trimmed | Where-Object { $_ -match '^\s*#{1,6}\s+' })
  $headingCount = if ($headings) { ($headings | Measure-Object).Count } else { 0 }
  $longLines = ($trimmed | Where-Object { $_.Length -gt 140 })
  $longLinesCount = if ($longLines) { ($longLines | Measure-Object).Count } else { 0 }

  # Duplicate lines within file (consider only lines > 40 chars)
  $dupesWithin = $trimmed |
    Where-Object { $_ -ne '' -and $_.Length -gt 40 } |
    Group-Object |
    Where-Object { $_.Count -gt 1 } |
    Sort-Object Count -Descending |
    Select-Object -First 5

  [pscustomobject]@{
    Path = $Path
    Lines = $lineCount
    Words = $wordCount
    Headings = $headingCount
    LongLines = $longLinesCount
    LongLineSamples = $longLines | Select-Object -First 2
    DupesWithin = $dupesWithin
    AllLines = $trimmed
  }
}

# Expand globs
$files = @()
foreach ($p in $Paths) {
  $files += Get-ChildItem -Path $p -File -ErrorAction SilentlyContinue
}
$files = $files | Sort-Object -Property FullName -Unique

if (-not $files -or $files.Count -eq 0) {
  Write-Host 'No files matched.' -ForegroundColor Yellow
  exit 0
}

$stats = foreach ($f in $files) { Get-FileStats -Path $f.FullName }

# Cross-file repeated lines (lines > 60 chars appearing in >=2 files)
$lineMap = @{}
foreach ($s in $stats) {
  foreach ($ln in $s.AllLines) {
    if ([string]::IsNullOrWhiteSpace($ln)) { continue }
    if ($ln.Length -lt 60) { continue }
    $key = $ln
    if (-not $lineMap.ContainsKey($key)) { $lineMap[$key] = @() }
    $lineMap[$key] += $s.Path
  }
}

$crossDupes = @()
foreach ($k in $lineMap.Keys) {
  $paths = $lineMap[$k] | Sort-Object -Unique
  if ($paths.Count -ge 2) {
    $crossDupes += [pscustomobject]@{ Text = $k; Files = $paths; Count = $paths.Count }
  }
}
$crossDupes = $crossDupes | Sort-Object -Property Count -Descending | Select-Object -First 10

function Render-Report {
  param($stats, $crossDupes)
  $out = @()
  $out += '# Claude Files Audit'
  $out += ''
  $out += ('Date: ' + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'))
  $out += ('Files: ' + (($stats.Path | Select-Object -Unique) -join ', '))
  $out += ''
  $out += '## Summary'
  foreach ($s in $stats) {
    $note = @()
    if ($s.Words -gt 1500) { $note += 'verbose' }
    if ($s.LongLines -gt 30) { $note += 'many long lines' }
    $noteStr = if ($note.Count -gt 0) { ' - ' + ($note -join ', ') } else { '' }
    $out += "- $($s.Path): lines=$($s.Lines), words=$($s.Words), headings=$($s.Headings), longLines=$($s.LongLines)$noteStr"
  }
  $out += ''
  $out += '## Within-file Duplicates (top 5 each)'
  foreach ($s in $stats) {
    $out += ("### " + $s.Path)
    if (-not $s.DupesWithin -or $s.DupesWithin.Count -eq 0) {
      $out += '(none)'
      continue
    }
    foreach ($g in $s.DupesWithin) {
      $sample = $g.Group[0]
      $out += "- ($($g.Count)x) $sample"
    }
  }
  $out += ''
  $out += '## Cross-file Repeated Lines (top 10)'
  if (-not $crossDupes -or $crossDupes.Count -eq 0) {
    $out += '(none)'
  } else {
    foreach ($d in $crossDupes) {
      $out += "- ($($d.Count) files) $($d.Text)"
    }
  }
  $out += ''
  $out += '## Suggestions'
  $out += '- Shorten verbose blocks (many lines > 140 chars).'
  $out += '- Move repeated phrasing to a single source (AGENTS.md) and link out.'
  $out += '- Keep one canonical rule set; reference it from agent files.'
  ($out -join "`n")
}

$report = Render-Report -stats $stats -crossDupes $crossDupes

if ([string]::IsNullOrWhiteSpace($Output)) {
  Write-Output $report
} else {
  $dir = Split-Path -Parent $Output
  if ($dir -and -not (Test-Path -Path $dir)) { New-Item -Path $dir -ItemType Directory | Out-Null }
  Set-Content -Path $Output -Value $report -Encoding ASCII
  Write-Host ('Report written to ' + $Output) -ForegroundColor Green
}

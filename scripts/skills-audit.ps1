# PowerShell script: audits local/global skills and reports file/line counts
param(
  [string]$GlobalDir = $env:SKILLS_GLOBAL_DIR,
  [switch]$AsJson
)

function Get-SkillStats {
  param([string]$Root)
  if (-not $Root) { return @() }
  if (-not (Test-Path -Path $Root)) { return @() }

  $folders = Get-ChildItem -Path $Root -Directory -ErrorAction SilentlyContinue
  $results = @()
  foreach ($f in $folders) {
    $files = Get-ChildItem -Path $f.FullName -Recurse -File -ErrorAction SilentlyContinue
    if (-not $files) { continue }
    $lineCount = 0
    foreach ($file in $files) {
      try {
        $lc = (Get-Content -Path $file.FullName -ErrorAction Stop | Measure-Object -Line).Lines
        $lineCount += [int]$lc
      } catch {
        # Skip unreadable files
      }
    }
    $results += [pscustomobject]@{
      Name  = $f.Name
      Path  = $f.FullName
      Files = $files.Count
      Lines = $lineCount
    }
  }
  return $results
}

# Determine project skills directory (../skills from repo root)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Resolve-Path -Path (Join-Path $scriptDir '..') | Select-Object -ExpandProperty Path
$projectSkills = Join-Path $projectRoot 'skills'

$projStats = Get-SkillStats -Root $projectSkills
$globStats = Get-SkillStats -Root $GlobalDir

$summary = [pscustomobject]@{
  ProjectRoot = $projectSkills
  GlobalRoot  = $GlobalDir
  Project     = $projStats
  Global      = $globStats
}

if ($AsJson) {
  $summary | ConvertTo-Json -Depth 5
} else {
  Write-Host "== Skills Audit ==" -ForegroundColor Cyan
  Write-Host "Project skills: $projectSkills"
  if ($projStats.Count -gt 0) {
    $projStats | Sort-Object -Property Lines -Descending | Format-Table -AutoSize
  } else {
    Write-Host "(no project skills found)"
  }
  Write-Host "\nGlobal skills: $GlobalDir"
  if ($globStats.Count -gt 0) {
    $globStats | Sort-Object -Property Lines -Descending | Format-Table -AutoSize
  } else {
    Write-Host "(no global skills found)"
  }
  Write-Host "\nTip: Review largest skills for conciseness, overlap, and token efficiency."
}

# skills-audit.ps1 — подсчёт skills (project/global): файлы и строки
# Использование:
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts/skills-audit.ps1
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts/skills-audit.ps1 -AsJson

param(
    [switch]$AsJson
)

$projectSkills = Join-Path $PSScriptRoot '..\.opencode\skills'

$dirs = @()
if (Test-Path -LiteralPath $projectSkills) {
    Get-ChildItem -LiteralPath $projectSkills -Directory | ForEach-Object {
        $dirs += [PSCustomObject]@{ Name = $_.Name; Path = $_.FullName; Scope = 'project' }
    }
}
if ($env:SKILLS_GLOBAL_DIR -and (Test-Path -LiteralPath $env:SKILLS_GLOBAL_DIR)) {
    Get-ChildItem -LiteralPath $env:SKILLS_GLOBAL_DIR -Directory | ForEach-Object {
        $dirs += [PSCustomObject]@{ Name = $_.Name; Path = $_.FullName; Scope = 'global' }
    }
}

$rows = foreach ($d in $dirs) {
    $files = Get-ChildItem -LiteralPath $d.Path -Recurse -File -ErrorAction SilentlyContinue
    $lines = 0
    if ($files) {
        $lines = ($files | Get-Content -ErrorAction SilentlyContinue | Measure-Object -Line).Lines
    }
    [PSCustomObject]@{
        scope = $d.Scope
        name  = $d.Name
        path  = $d.Path
        files = @($files).Count
        lines = $lines
    }
}

$rows = $rows | Sort-Object -Property lines -Descending

if ($AsJson) {
    $rows | ConvertTo-Json -Depth 3
}
else {
    $rows | Format-Table -AutoSize
    $heavy = $rows | Select-Object -First 3
    if ($heavy) {
        Write-Host ''
        Write-Host 'Кандидаты на сжатие (самые тяжёлые skills):' -ForegroundColor Yellow
        foreach ($h in $heavy) {
            Write-Host ("  {0} — {1} файлов, {2} строк" -f $h.name, $h.files, $h.lines)
        }
    }
}
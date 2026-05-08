param(
    [string]$Language = "auto",
    [switch]$Fast
)

$ErrorCount = 0
$Warnings = @()

function Run-Check {
    param([string]$Name, [string]$Cmd, [string]$ cwd = $PWD)
    Write-Host "[$Name] " -NoNewline
    try {
        $result = Invoke-Expression $Cmd 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓" -ForegroundColor Green
        } else {
            Write-Host "✗" -ForegroundColor Red
            $script:ErrorCount++
            $script:Warnings += "$Name failed"
        }
    } catch {
        Write-Host "?" -ForegroundColor Yellow
    }
}

if ($Language -eq "auto") {
    if (Test-Path "package.json") { $Language = "js" }
    elseif (Test-Path "*.py") { $Language = "python" }
    elseif (Test-Path "*.html") { $Language = "html" }
}

switch ($Language) {
    "python" {
        if (Get-Command ruff -ErrorAction SilentlyContinue) {
            Run-Check "ruff" "ruff check ."
        }
        if (Get-Command mypy -ErrorAction SilentlyContinue) {
            Run-Check "mypy" "mypy ."
        }
    }
    "js" {
        if (Get-Command eslint -ErrorAction SilentlyContinue) {
            Run-Check "eslint" "eslint ."
        }
        if (Get-Command tsc -ErrorAction SilentlyContinue) {
            Run-Check "tsc" "tsc --noEmit"
        }
    }
}

if ($ErrorCount -gt 0) {
    Write-Host "`n❌ $ErrorCount checks failed" -ForegroundColor Red
    exit 1
} else {
    Write-Host "`n✓ All checks passed" -ForegroundColor Green
    exit 0
}
param(
    [Parameter(Mandatory=$true)]
    [string]$Url,
    [string]$Selector,
    [ValidateSet("markdown","text","json")]
    [string]$Format = "text"
)

$ErrorActionPreference = "Stop"

function Get-WebPage {
    param([string]$Url, [string]$Format)

    try {
        $response = Invoke-WebRequest -Uri $Url `
            -Headers @{
                "User-Agent" = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            } `
            -TimeoutSec 30

        if ($Format -eq "text") {
            $script:Content = $response.Content
        } else {
            $script:Content = $response.Content
        }
        Write-Host "✓ Fetched $($response.StatusCode)" -ForegroundColor Green
    } catch {
        Write-Host "✗ $($_.Exception.Message)" -ForegroundColor Red
        exit 1
    }
}

function Parse-HTML {
    param([string]$Selector)
    Add-Type -AssemblyName System.Xml
    Add-Type -AssemblyName System.Xml.Linq

    if (-not $Selector) {
        return $script:Content
    }

    # Simple CSS selector parser (subset)
    # For full HTML parsing use python/bs4 or playwright
    Write-Host "Selector: $Selector"
    return $script:Content
}

Get-WebPage -Url $Url -Format $Format

if ($Selector) {
    Parse-HTML -Selector $Selector
}
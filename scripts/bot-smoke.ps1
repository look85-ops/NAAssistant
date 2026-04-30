# Smoke test for Bot MVP deployment
param(
  [string]$BaseUrl = 'http://localhost:8000',
  [string]$Prompt = 'Сформулируй 2 тезиса о снижении галлюцинаций через CLI-контекст'
)

try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch {}

Write-Host "[1/2] GET /health" -ForegroundColor Cyan
try {
  $health = Invoke-RestMethod -Method Get -Uri "$BaseUrl/health" -TimeoutSec 10
  Write-Host ("Health: " + ($health | ConvertTo-Json -Compress)) -ForegroundColor Green
} catch {
  Write-Error "Health check failed: $_"; exit 1
}

Write-Host "[2/2] POST /api/chat" -ForegroundColor Cyan
$body = @{ message = $Prompt } | ConvertTo-Json -Depth 5
try {
  $chat = Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/chat" -ContentType 'application/json; charset=utf-8' -Body $body -TimeoutSec 45
  $out = $chat.output
  if (-not $out) { $out = ($chat | ConvertTo-Json -Compress) }
  Write-Host "Model: $($chat.model)" -ForegroundColor Yellow
  Write-Host "Output:" -ForegroundColor Yellow
  Write-Output $out
} catch {
  Write-Error "Chat request failed: $_"; exit 2
}

Write-Host "Smoke test passed" -ForegroundColor Green

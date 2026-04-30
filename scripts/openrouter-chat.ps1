# Simple chat.completions test for OpenRouter (OpenAI-compatible)
param(
  [string]$Model = 'meta-llama/llama-3.1-8b-instruct',
  [string]$Prompt = 'Say hello in one sentence.'
)

if (-not $env:OPENROUTER_API_KEY) {
  # Try to read from local file if provided
  $keyFile = Join-Path -Path (Get-Location) -ChildPath 'api_openrouter.txt'
  if (Test-Path -Path $keyFile) {
    $env:OPENROUTER_API_KEY = (Get-Content -Path $keyFile -Raw).Trim()
  }
}

if (-not $env:OPENROUTER_API_KEY) {
  Write-Error 'OPENROUTER_API_KEY is not set and api_openrouter.txt not found.'
  exit 1
}

$body = @{ 
  model = $Model
  messages = @(@{ role = 'user'; content = $Prompt })
} | ConvertTo-Json -Depth 5

$headers = @{ 
  'Authorization' = "Bearer $($env:OPENROUTER_API_KEY)" 
  'Content-Type'  = 'application/json' 
}

$url = 'https://openrouter.ai/api/v1/chat/completions'

try {
  $res = Invoke-RestMethod -Method Post -Uri $url -Headers $headers -Body $body -TimeoutSec 30
  $text = $res.choices[0].message.content
  Write-Output $text
} catch {
  Write-Error $_
  exit 2
}

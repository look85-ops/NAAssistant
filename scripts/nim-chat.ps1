# Simple chat.completions test for NVIDIA NIM (OpenAI-compatible)
param(
  [string]$Model = 'meta/llama-3.1-8b-instruct',
  [string]$Prompt = 'Say hello in 1 sentence.'
)

if (-not $env:NVIDIA_API_KEY) {
  Write-Error 'NVIDIA_API_KEY is not set.'
  exit 1
}

$body = @{ 
  model = $Model
  messages = @(@{ role = 'user'; content = $Prompt })
} | ConvertTo-Json -Depth 5

$headers = @{ 
  'Authorization' = "Bearer $($env:NVIDIA_API_KEY)" 
  'Content-Type'  = 'application/json' 
}

$url = 'https://integrate.api.nvidia.com/v1/chat/completions'

try {
  $res = Invoke-RestMethod -Method Post -Uri $url -Headers $headers -Body $body -TimeoutSec 30
  $text = $res.choices[0].message.content
  Write-Output $text
} catch {
  Write-Error $_
  exit 2
}

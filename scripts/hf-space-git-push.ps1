# Pushes hf_space/ contents to an existing Hugging Face Space via git
param(
  [Parameter(Mandatory=$true)][string]$User,
  [Parameter(Mandatory=$true)][string]$Space,
  [Parameter(Mandatory=$true)][string]$TokenPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if (-not (Test-Path -Path $TokenPath)) { throw "Token file not found: $TokenPath" }
$token = (Get-Content -Raw $TokenPath).Trim()
if (-not $token) { throw 'Token file is empty' }

$repoUrl = "https://huggingface.co/spaces/$User/$Space"
$tmp = Join-Path (Get-Location) ("_hf_push_" + ([System.Guid]::NewGuid().ToString('N')))

git clone $repoUrl $tmp | Out-Null

Copy-Item -Path 'hf_space/app.py' -Destination (Join-Path $tmp 'app.py') -Force
Copy-Item -Path 'hf_space/requirements.txt' -Destination (Join-Path $tmp 'requirements.txt') -Force
if (Test-Path 'hf_space/Dockerfile') {
  Copy-Item -Path 'hf_space/Dockerfile' -Destination (Join-Path $tmp 'Dockerfile') -Force
}

Push-Location $tmp
git config user.email 'deploy@example.com'
git config user.name 'HF Deploy'
git add .
git commit -m 'Deploy FastAPI bot MVP' | Out-Null

# Temporarily store credentials
$credFile = Join-Path $env:USERPROFILE '.git-credentials'
$credLine = "https://$($User):$($token)@huggingface.co"
Set-Content -Path $credFile -Value $credLine -Encoding ASCII
git config credential.helper store

git push

# Cleanup
Remove-Item $credFile -Force
git config --unset credential.helper
Pop-Location

Write-Host "Pushed to $repoUrl" -ForegroundColor Green

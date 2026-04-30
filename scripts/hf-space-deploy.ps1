# Deploys hf_space/ FastAPI app to a new Hugging Face Space
param(
  [Parameter(Mandatory=$true)][string]$User,        # HF username or org
  [Parameter(Mandatory=$true)][string]$Space,       # Space name (slug)
  [string]$Token = $env:HUGGINGFACE_TOKEN,          # HF token (write)
  [switch]$Private,                                 # Make space private
  [string]$Sdk = 'fastapi'                          # Space SDK
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Ensure-HFCLI {
  try { huggingface-cli --version | Out-Null } catch {
    Write-Host 'Installing huggingface_hub (huggingface-cli)...' -ForegroundColor Cyan
    python -m pip install --upgrade huggingface_hub | Out-Null
  }
}

function HF-Login {
  param([string]$tok)
  if (-not $tok) { throw 'Hugging Face token is required. Provide -Token or set HUGGINGFACE_TOKEN.' }
  huggingface-cli login --token $tok --add-to-git-credential | Out-Null
}

function HF-CreateSpace {
  param([string]$repo, [string]$sdk, [switch]$priv)
  $flags = @('--type','space','--sdk', $sdk, '--yes')
  if ($priv) { $flags += '--private' }
  try {
    huggingface-cli repo create $repo @flags | Out-Null
  } catch {
    Write-Host 'Repo may already exist, continuing...' -ForegroundColor Yellow
  }
}

function Copy-AppFiles {
  param([string]$dst)
  Copy-Item -Path 'hf_space/app.py' -Destination (Join-Path $dst 'app.py') -Force
  Copy-Item -Path 'hf_space/requirements.txt' -Destination (Join-Path $dst 'requirements.txt') -Force
}

# Main
Ensure-HFCLI
HF-Login -tok $Token

$repoId = "$User/$Space"
HF-CreateSpace -repo $repoId -sdk $Sdk -priv:$Private

$tmp = Join-Path (Get-Location) "_hf_space_$Space"
if (Test-Path $tmp) { Remove-Item -Recurse -Force $tmp }
git clone "https://huggingface.co/spaces/$repoId" $tmp | Out-Null

Copy-AppFiles -dst $tmp

Push-Location $tmp
git add .
git commit -m "Init FastAPI bot MVP"
git push
Pop-Location

$url = "https://huggingface.co/spaces/$repoId"
Write-Host "Space deployed: $url" -ForegroundColor Green

# Prompt length linter hook
param(
  [string]$Text
)

if ($env:HOOK_PROMPT_LINTER -eq '0') {
  if ($Text) { $Text } else { [Console]::In.ReadToEnd() }
  exit 0
}

function Get-InputText {
  param([string]$T)
  if ($T) { return $T }
  try { return [Console]::In.ReadToEnd() } catch { return '' }
}

$inputText = Get-InputText -T $Text
$words = ($inputText -split "\s+" | Where-Object { $_ -ne '' })
$count = $words.Count

if ($count -gt 50) {
  $note = "[Note] Проверьте, что желаемый результат сформулирован явно (1–2 предложения)."
  Write-Output ($inputText.TrimEnd() + "`n`n" + $note)
} else {
  Write-Output $inputText
}

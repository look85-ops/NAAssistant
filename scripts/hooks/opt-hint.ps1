# Optimization hint on heavy tool usage
param(
  [int]$ToolCalls,
  [string]$Text
)

if ($env:HOOK_OPT_HINT -eq '0') {
  if ($Text) { $Text } else { [Console]::In.ReadToEnd() }
  exit 0
}

function Get-InputText {
  param([string]$T)
  if ($T) { return $T }
  try { return [Console]::In.ReadToEnd() } catch { return '' }
}

$inputText = Get-InputText -T $Text
if (-not $ToolCalls) { $ToolCalls = 0 }

if ($ToolCalls -ge 8) {
  $hint = "[Hint] Вынесите повторяемые шаги в skill или сохраните промежуточные артефакты в память; это снизит токены и время."
  Write-Output ($inputText.TrimEnd() + "`n`n" + $hint)
} else {
  Write-Output $inputText
}

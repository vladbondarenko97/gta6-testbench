param([string]$Exe)
# Block ALL outbound traffic for a process that hosts guest code.
# Rationale: the title's built-in crash reporter uses host WinHttp directly and can upload
# multi-MB dumps even when the layer's own network switch is off (upstream: ivall/xcl#305).
$ErrorActionPreference = 'SilentlyContinue'
if (-not (Test-Path $Exe)) { Write-Error "not found: $Exe"; exit 1 }
$name = "Block guest outbound $(Split-Path $Exe -Leaf) @ $Exe"
New-NetFirewallRule -DisplayName $name -Direction Outbound -Program $Exe -Action Block -Profile Any | Out-Null
Write-Output "blocked outbound: $Exe"
Write-Output ("verify: " + (Get-NetFirewallRule -DisplayName $name | Select-Object -First 1).Enabled)

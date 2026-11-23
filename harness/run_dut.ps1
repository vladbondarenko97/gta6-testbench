param(
  [Parameter(Mandatory=$true)][ValidateSet('xcl','victory','percyscarlett')][string]$Dut,
  [Parameter(Mandatory=$true)][string]$Exe,
  [Parameter(Mandatory=$true)][string]$GameDir,
  [int]$Seconds = 240,
  [switch]$FrameDump,
  [switch]$Screenshots,
  [string]$OutDir = "$PSScriptRoot\..\out"
)
# Generic DUT runner. Launches the layer against the user's own copy, isolates network,
# captures logs and (optionally) frame dumps / desktop screenshots.
$ErrorActionPreference = 'Stop'
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'

# 1. network isolation for the DUT process
& "$PSScriptRoot\..\privacy\block_guest_network.ps1" -Exe $Exe | Out-Null

# 2. environment
$env:XCL_NETWORK = '0'
$env:XCL_ACTIVITY = '1'
if ($FrameDump) { $env:XCL_FRAME_DUMP = '60' }

# 3. launch
$out = Join-Path $OutDir "$Dut-$stamp.out"
$err = Join-Path $OutDir "$Dut-$stamp.err"
switch ($Dut) {
  'xcl'          { $argv = @('run', $GameDir) }
  'victory'      { $argv = @('run', (Join-Path $GameDir 'game_scarlett_master.exe'), '--execute') }
  'percyscarlett'{ $argv = @('run', (Join-Path $GameDir 'game_scarlett_master.exe')) }
}
$proc = Start-Process -FilePath $Exe -ArgumentList $argv -PassThru -RedirectStandardOutput $out -RedirectStandardError $err

if ($Screenshots) {
  Add-Type -AssemblyName System.Windows.Forms, System.Drawing
  $elapsed = 0
  foreach ($t in @(20, 40, 65, 95, 125)) {
    if ($t -gt $Seconds) { break }
    Start-Sleep -Seconds ($t - $elapsed); $elapsed = $t
    $b = [Windows.Forms.Screen]::PrimaryScreen.Bounds
    $bmp = New-Object Drawing.Bitmap $b.Width, $b.Height
    $g = [Drawing.Graphics]::FromImage($bmp)
    $g.CopyFromScreen($b.X, $b.Y, 0, 0, $bmp.Size)
    $bmp.Save((Join-Path $OutDir "shot_$t.png"), [Drawing.Imaging.ImageFormat]::Png)
    $g.Dispose(); $bmp.Dispose()
  }
  $remaining = $Seconds - $elapsed
  if ($remaining -gt 0) { Start-Sleep -Seconds $remaining }
} else {
  Start-Sleep -Seconds $Seconds
}

$alive = -not $proc.HasExited
if ($alive) { Stop-Process -Id $proc.Id -Force }
"$Dut run finished: alive_at_timeout=$alive"
"stdout: $out"
"stderr: $err"

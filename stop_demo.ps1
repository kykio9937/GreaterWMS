$projectRoot = 'E:\Desktop_Migrated_20260608\WMS-Demo'
$backendPython = Join-Path $projectRoot '.conda310\python.exe'
$frontendNode = 'C:\Program Files\nodejs\node.exe'
$frontendRoot = Join-Path $projectRoot 'templates'

$targets = Get-CimInstance Win32_Process | Where-Object {
  ($_.ExecutablePath -eq $backendPython -and $_.CommandLine -like '*manage.py*runserver*8008*') -or
  ($_.ExecutablePath -eq $frontendNode -and $_.CommandLine -like "*$frontendRoot*serve-spa.js*")
}

if (-not $targets) {
  Write-Host 'No running demo processes found.'
  exit 0
}

$targets | ForEach-Object {
  Stop-Process -Id $_.ProcessId -Force
  Write-Host ("Stopped process PID {0}" -f $_.ProcessId)
}

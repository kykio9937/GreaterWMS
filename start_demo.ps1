[CmdletBinding()]
param(
  [ValidateSet('yes', 'no')]
  [string]$OpenBrowser = 'yes',
  [string]$FrontendUrl = 'http://127.0.0.1:8080/#/'
)

$ErrorActionPreference = 'Stop'

$projectRoot = 'E:\Desktop_Migrated_20260608\WMS-Demo'
$backendPythonCandidates = @(
  (Join-Path $projectRoot '.conda310local\python.exe'),
  (Join-Path $projectRoot '.conda310local\Scripts\python.exe'),
  (Join-Path $projectRoot '.conda310\python.exe'),
  (Join-Path $projectRoot '.conda310\Scripts\python.exe'),
  'E:\minconda\python.exe'
)
$backendPython = $backendPythonCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1
$frontendNode = 'C:\Program Files\nodejs\node.exe'
$frontendRoot = Join-Path $projectRoot 'templates'

function Test-UrlOk {
  param(
    [string]$Url
  )

  try {
    $response = Invoke-WebRequest -UseBasicParsing $Url -TimeoutSec 5
    return $response.StatusCode -eq 200
  } catch {
    return $false
  }
}

if (-not $backendPython) {
  throw "未找到可用的后端 Python 环境，已检查: $($backendPythonCandidates -join ', ')"
}

if (-not (Test-Path $frontendNode)) {
  throw "未找到前端 Node 环境: $frontendNode"
}

if (-not (Test-UrlOk 'http://127.0.0.1:8008')) {
  Start-Process -FilePath $backendPython `
    -ArgumentList 'manage.py', 'runserver', '0.0.0.0:8008' `
    -WorkingDirectory $projectRoot `
    -WindowStyle Hidden
  Start-Sleep -Seconds 8
}

if (-not (Test-UrlOk 'http://127.0.0.1:8080')) {
  Start-Process -FilePath $frontendNode `
    -ArgumentList 'serve-spa.js' `
    -WorkingDirectory $frontendRoot `
    -WindowStyle Hidden
  Start-Sleep -Seconds 4
}

$backendOk = Test-UrlOk 'http://127.0.0.1:8008'
$frontendOk = Test-UrlOk 'http://127.0.0.1:8080'

Write-Host "后端 8008: $backendOk"
Write-Host "前端 8080: $frontendOk"
Write-Host "访问地址: $FrontendUrl"

if ($backendOk -and $frontendOk -and $OpenBrowser -eq 'yes') {
  Start-Process $FrontendUrl | Out-Null
}


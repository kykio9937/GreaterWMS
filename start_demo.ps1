[CmdletBinding()]
param(
  [ValidateSet('yes', 'no')]
  [string]$OpenBrowser = 'yes',
  [string]$FrontendUrl = 'http://127.0.0.1:8080/#/'
)

$ErrorActionPreference = 'Stop'

$projectRoot = 'E:\Desktop_Migrated_20260608\WMS-Demo'
$runtimeDir = Join-Path $projectRoot '.demo-runtime'
$backendPidFile = Join-Path $runtimeDir 'backend.pid'
$frontendPidFile = Join-Path $runtimeDir 'frontend.pid'
$backendOutLog = Join-Path $runtimeDir 'backend.out.log'
$backendErrLog = Join-Path $runtimeDir 'backend.err.log'
$frontendOutLog = Join-Path $runtimeDir 'frontend.out.log'
$frontendErrLog = Join-Path $runtimeDir 'frontend.err.log'
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
$frontendPs = "$env:SystemRoot\System32\WindowsPowerShell\v1.0\powershell.exe"

function Ensure-RuntimeDir {
  if (-not (Test-Path $runtimeDir)) {
    New-Item -ItemType Directory -Path $runtimeDir | Out-Null
  }
}

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

function Get-RunningProcessFromPidFile {
  param(
    [string]$PidFile
  )

  if (-not (Test-Path $PidFile)) {
    return $null
  }

  $rawPid = (Get-Content -Path $PidFile -ErrorAction SilentlyContinue | Select-Object -First 1).Trim()
  if (-not $rawPid) {
    return $null
  }

  $process = Get-Process -Id ([int]$rawPid) -ErrorAction SilentlyContinue
  if ($process) {
    return $process
  }

  Remove-Item -LiteralPath $PidFile -Force -ErrorAction SilentlyContinue
  return $null
}

function Wait-ForUrl {
  param(
    [string]$Url,
    [int]$Seconds = 20
  )

  for ($i = 0; $i -lt $Seconds; $i++) {
    if (Test-UrlOk $Url) {
      return $true
    }
    Start-Sleep -Seconds 1
  }

  return $false
}

function Start-BackendServer {
  $process = Start-Process -FilePath $backendPython `
    -ArgumentList 'manage.py', 'runserver', '0.0.0.0:8008' `
    -WorkingDirectory $projectRoot `
    -RedirectStandardOutput $backendOutLog `
    -RedirectStandardError $backendErrLog `
    -WindowStyle Hidden `
    -PassThru
  Set-Content -Path $backendPidFile -Value $process.Id
  return $process
}

function Start-FrontendServer {
  $process = Start-Process -FilePath $frontendNode `
    -ArgumentList 'serve-spa.js' `
    -WorkingDirectory $frontendRoot `
    -RedirectStandardOutput $frontendOutLog `
    -RedirectStandardError $frontendErrLog `
    -WindowStyle Hidden `
    -PassThru
  Set-Content -Path $frontendPidFile -Value $process.Id
  return $process
}

if (-not $backendPython) {
  throw 'No backend Python runtime found.'
}

if (-not (Test-Path $frontendNode)) {
  throw "Frontend Node runtime not found: $frontendNode"
}

if (-not (Test-Path $frontendPs)) {
  throw "PowerShell runtime not found: $frontendPs"
}

Ensure-RuntimeDir

$backendProcess = Get-RunningProcessFromPidFile -PidFile $backendPidFile
$frontendProcess = Get-RunningProcessFromPidFile -PidFile $frontendPidFile

if (-not (Test-UrlOk 'http://127.0.0.1:8008')) {
  if (-not $backendProcess) {
    $backendProcess = Start-BackendServer
  }
  [void](Wait-ForUrl -Url 'http://127.0.0.1:8008' -Seconds 20)
}

if (-not (Test-UrlOk 'http://127.0.0.1:8080')) {
  if (-not $frontendProcess) {
    $frontendProcess = Start-FrontendServer
  }
  [void](Wait-ForUrl -Url 'http://127.0.0.1:8080' -Seconds 20)
}

$backendOk = Test-UrlOk 'http://127.0.0.1:8008'
$frontendOk = Test-UrlOk 'http://127.0.0.1:8080'

Write-Host "Backend 8008: $backendOk"
Write-Host "Frontend 8080: $frontendOk"
Write-Host "URL: $FrontendUrl"

if ($backendOk -and $frontendOk -and $OpenBrowser -eq 'yes') {
  Start-Process $FrontendUrl | Out-Null
}

if (-not $backendOk) {
  Write-Host "Backend log: $backendErrLog"
}

if (-not $frontendOk) {
  Write-Host "Frontend log: $frontendErrLog"
}

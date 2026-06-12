$projectRoot = 'E:\Desktop_Migrated_20260608\WMS-Demo'
$runtimeDir = Join-Path $projectRoot '.demo-runtime'
$backendPidFile = Join-Path $runtimeDir 'backend.pid'
$frontendPidFile = Join-Path $runtimeDir 'frontend.pid'

function Stop-ProcessByPidFile {
  param(
    [string]$PidFile,
    [string]$Label
  )

  if (-not (Test-Path $PidFile)) {
    return $false
  }

  $rawPid = (Get-Content -Path $PidFile -ErrorAction SilentlyContinue | Select-Object -First 1).Trim()
  if (-not $rawPid) {
    Remove-Item -LiteralPath $PidFile -Force -ErrorAction SilentlyContinue
    return $false
  }

  $process = Get-Process -Id ([int]$rawPid) -ErrorAction SilentlyContinue
  if ($process) {
    Stop-Process -Id $process.Id -Force
    Write-Host ("Stopped {0} PID {1}" -f $Label, $process.Id)
  }

  Remove-Item -LiteralPath $PidFile -Force -ErrorAction SilentlyContinue
  return [bool]$process
}

$stoppedBackend = Stop-ProcessByPidFile -PidFile $backendPidFile -Label 'backend'
$stoppedFrontend = Stop-ProcessByPidFile -PidFile $frontendPidFile -Label 'frontend'

if (-not $stoppedBackend -and -not $stoppedFrontend) {
  Write-Host 'No running demo processes found.'
}

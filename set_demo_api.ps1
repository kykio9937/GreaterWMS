[CmdletBinding()]
param(
  [Parameter(Mandatory = $true)]
  [string]$ApiBaseUrl
)

$ErrorActionPreference = 'Stop'

$projectRoot = 'E:\Desktop_Migrated_20260608\GreaterWMS-master'
$baseUrlFiles = @(
  (Join-Path $projectRoot 'templates\public\statics\baseurl.txt'),
  (Join-Path $projectRoot 'templates\dist\spa\statics\baseurl.txt')
)

if (-not $ApiBaseUrl.Trim()) {
  throw 'ApiBaseUrl 不能为空'
}

$normalized = $ApiBaseUrl.Trim()

foreach ($baseUrlFile in $baseUrlFiles) {
  if (Test-Path $baseUrlFile) {
    Set-Content -Path $baseUrlFile -Value $normalized -Encoding UTF8
    Write-Host "已更新接口地址: $baseUrlFile"
  }
}

Write-Host "当前演示接口地址: $normalized"

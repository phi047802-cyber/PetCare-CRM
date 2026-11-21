param(
    [string]$FrappeDockerPath = $env:FRAPPE_DOCKER_PATH
)

$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($FrappeDockerPath)) {
    throw "Set FRAPPE_DOCKER_PATH or pass -FrappeDockerPath with the frappe_docker repository path."
}

$resolvedFrappeDockerPath = (Resolve-Path -LiteralPath $FrappeDockerPath).Path
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    throw "Docker CLI was not found in PATH."
}

Push-Location -LiteralPath $resolvedFrappeDockerPath
try {
    if (-not (Test-Path -LiteralPath "apps.json" -PathType Leaf)) {
        throw "apps.json was not found in $resolvedFrappeDockerPath."
    }

    $appsJson = Get-Content -LiteralPath "apps.json" -Raw
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($appsJson)
    $appsJsonBase64 = [Convert]::ToBase64String($bytes)
    docker build --secret id=apps_json,src=apps.json --build-arg "APPS_JSON_BASE64=$appsJsonBase64" --tag petcare-frappe:latest --file images/custom/Containerfile .
    if ($LASTEXITCODE -ne 0) {
        throw "Docker image build failed with exit code $LASTEXITCODE."
    }
}
finally {
    Pop-Location
}


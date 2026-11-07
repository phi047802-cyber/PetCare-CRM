$env:PATH += ";C:\Users\pc\AppData\Local\Atlassian\SourceTree\git_local\cmd"
Set-Location D:\data\frappe_docker
$appsJson = Get-Content apps.json -Raw
$bytes = [System.Text.Encoding]::UTF8.GetBytes($appsJson)
$env:APPS_JSON_BASE64 = [Convert]::ToBase64String($bytes)
docker build --secret id=apps_json,src=apps.json --build-arg APPS_JSON_BASE64=$env:APPS_JSON_BASE64 --tag petcare-frappe:latest --file images/custom/Containerfile .


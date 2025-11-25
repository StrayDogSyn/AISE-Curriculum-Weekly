<#
Start a local Postgres container for this repo using Docker.
Usage: .\start-postgres-docker.ps1 [-User <string>] [-Password <string>] [-DB <string>]
#>
param(
    [string]$User = "aise_admin",
    [string]$Password = "aise_password",
    [string]$DB = "aise_db"
)

Write-Host "Checking for Docker..."
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Error "Docker CLI not found. Install Docker Desktop for Windows and try again: https://www.docker.com/products/docker-desktop"
    exit 1
}

$compose = Join-Path -Path $PSScriptRoot -ChildPath "..\devtools\docker-compose.postgres.yml"
if (-not (Test-Path $compose)) {
    Write-Error "docker-compose file not found at $compose"
    exit 1
}

Write-Host "Starting Postgres container via docker-compose..."
# Use docker compose if available, otherwise fallback to docker-compose
if (Get-Command 'docker' -ErrorAction SilentlyContinue) {
    docker compose -f $compose up -d
} else {
    docker-compose -f $compose up -d
}

Write-Host "Postgres started (exposed on localhost:5432). Default credentials:"
Write-Host "  user: $User"
Write-Host "  password: $Password"
Write-Host "  db: $DB"
Write-Host "To stop: docker compose -f $compose down -v"

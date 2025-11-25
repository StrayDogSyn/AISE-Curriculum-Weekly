<#
Initialize Postgres database and user using psql (native install) or by connecting to running container.
Usage examples:
  # Using native psql (Windows installer) - you will be prompted for password if required
  .\init-db.ps1 -HostName localhost -Port 5432 -AdminUser postgres -AdminPassword your_postgres_password -NewUser aise_admin -NewPassword aise_password -NewDB aise_db

  # If using the Docker container above, defaults will work without admin password
  .\init-db.ps1
#>
param(
    [string]$HostName = "localhost",
    [int]$Port = 5432,
    [string]$AdminUser = "postgres",
    [string]$AdminPassword = "",
    [string]$NewUser = "aise_admin",
    [string]$NewPassword = "aise_password",
    [string]$NewDB = "aise_db"
)

function Invoke-DBCommand {
    param([string]$Sql)
    $env:PGPASSWORD = $AdminPassword
    $escaped = $Sql.Replace('"','\"')
    $cmd = "psql -h $HostName -p $Port -U $AdminUser -d postgres -c \"$escaped\""
    Write-Host "Running: $cmd"
    & cmd /c $cmd
    if ($LASTEXITCODE -ne 0) {
        Write-Error "psql reported exit code $LASTEXITCODE"
        exit $LASTEXITCODE
    }
}

# Check for psql
if (-not (Get-Command psql -ErrorAction SilentlyContinue)) {
    Write-Warning "psql not found in PATH. If you're using Docker run the Docker helper script."
    Write-Host "You can install Postgres for Windows from https://www.postgresql.org/download/windows/ or use the Docker helper: scripts\start-postgres-docker.ps1"
    exit 1
}

# Create user (if not exists) and database (if not exists)
$sqlCreateUser = "DO $$ BEGIN IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '$NewUser') THEN CREATE ROLE $NewUser WITH LOGIN PASSWORD '$NewPassword'; END IF; END $$;"
$sqlCreateDB = "DO $$ BEGIN IF NOT EXISTS (SELECT FROM pg_database WHERE datname = '$NewDB') THEN CREATE DATABASE $NewDB OWNER $NewUser; END IF; END $$;"

Invoke-DBCommand -Sql $sqlCreateUser
Invoke-DBCommand -Sql $sqlCreateDB

Write-Host "Done. Created/verified user '$NewUser' and database '$NewDB' on ${HostName}:$Port"

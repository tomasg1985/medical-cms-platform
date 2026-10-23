$ErrorActionPreference = "Stop"

$Backend = Join-Path (Get-Location).Path "backend"
if (-not (Test-Path $Backend)) {
    throw "Run this script from the repository root."
}

$ReportDir = Join-Path $Backend "reports"
$ReportFile = Join-Path $ReportDir "grupo3_auditoria.txt"
New-Item -ItemType Directory -Path $ReportDir -Force | Out-Null

$Lines = [System.Collections.Generic.List[string]]::new()
$Lines.Add("MEDICAL CMS - GROUP 3 STATIC AUDIT")
$Lines.Add("Date: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')")
$Lines.Add("Read-only inventory. No tests or migrations executed.")

$Sections = @(
    @{ Title = "ROUTES"; Path = "app/routes"; Pattern = '@router\.(get|post|put|patch|delete)|HTTPException|response_model|status_code' },
    @{ Title = "SERVICES"; Path = "app/services"; Pattern = 'def |async def |repository|commit\(|rollback\(|raise ' },
    @{ Title = "REPOSITORIES"; Path = "app/repositories"; Pattern = 'def |select\(|add\(|commit\(|rollback\(|delete\(|execute\(' },
    @{ Title = "SCHEMAS"; Path = "app/schemas"; Pattern = 'class |Field\(|ConfigDict|validator|EmailStr' },
    @{ Title = "MODELS"; Path = "app/models"; Pattern = '__tablename__|mapped_column|ForeignKey|relationship\(|UniqueConstraint|nullable=|primary_key=' },
    @{ Title = "TESTS"; Path = "tests"; Pattern = 'def test_|async def test_|client\.(get|post|put|patch|delete)|assert |medical_cms_test|create_all' },
    @{ Title = "MIGRATIONS"; Path = "alembic/versions"; Pattern = '^revision\s*=|^down_revision\s*=|def upgrade|def downgrade|op\.|pass$' }
)

foreach ($Section in $Sections) {
    $Lines.Add("")
    $Lines.Add(("=" * 60))
    $Lines.Add($Section.Title)
    $Lines.Add(("=" * 60))

    $Folder = Join-Path $Backend $Section.Path
    if (-not (Test-Path $Folder)) {
        $Lines.Add("Folder not found: $($Section.Path)")
        continue
    }

    Get-ChildItem $Folder -Recurse -File -Filter "*.py" |
        Where-Object { $_.FullName -notmatch '\\(__pycache__|\.venv|venv|node_modules)\\' } |
        Sort-Object FullName |
        ForEach-Object {
            $File = $_
            $Relative = $File.FullName.Substring($Backend.Length + 1)
            $Lines.Add("")
            $Lines.Add("FILE: $Relative ($($File.Length) bytes)")

            if ($File.Length -eq 0) {
                $Lines.Add("WARNING: EMPTY FILE")
            }
            else {
                Select-String -Path $File.FullName -Pattern $Section.Pattern |
                    ForEach-Object {
                        $Lines.Add(("  L{0}: {1}" -f $_.LineNumber, $_.Line.Trim()))
                    }
            }
        }
}

$Lines.Add("")
$Lines.Add(("=" * 60))
$Lines.Add("EMPTY PYTHON FILES")
$Lines.Add(("=" * 60))

Get-ChildItem $Backend -Recurse -File -Filter "*.py" |
    Where-Object {
        $_.FullName -notmatch '\\(__pycache__|\.venv|venv|node_modules)\\' -and
        $_.Length -eq 0
    } |
    ForEach-Object {
        $Lines.Add($_.FullName.Substring($Backend.Length + 1))
    }

[System.IO.File]::WriteAllLines(
    $ReportFile,
    $Lines,
    [System.Text.UTF8Encoding]::new($false)
)

Write-Host "Static audit finished."
Write-Host "Report: $ReportFile"
Write-Host "No tests or migrations were executed."
param(
    [string]$Message = ""
)

$status = git status --porcelain
if (-not $status) {
    Write-Host "No changes to commit."
    exit 0
}

if (-not $Message) {
    $Message = "chore: automated sync update"
}

git add -A
git commit -m "$Message"
git push origin HEAD

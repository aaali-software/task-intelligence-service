Param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$Args
)

if (Test-Path .venv\Scripts\Activate.ps1) {
    & .venv\Scripts\Activate.ps1
    python -m pytest @Args
    exit $LASTEXITCODE
} else {
    python -m pytest @Args
    exit $LASTEXITCODE
}

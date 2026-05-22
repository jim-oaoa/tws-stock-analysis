# 使用 hermes 根目錄 venv 執行專案指令
# 若出現「已停用指令碼執行」，請改用 run.cmd，或：
#   powershell -ExecutionPolicy Bypass -File run.ps1 test
param(
    [Parameter(Position = 0)]
    [ValidateSet("seed", "test", "api", "lint")]
    [string]$Command = "test"
)

$Python = "d:\AI\hermes\venv\Scripts\python.exe"
$Root = "d:\AI\hermes\Projects\tws-stock-analysis"
Set-Location $Root

switch ($Command) {
    "seed" { & $Python scripts/seed_db.py }
    "test" { & $Python -m pytest -q }
    "api"  { & $Python -m uvicorn src.api.main:app --reload --host 127.0.0.1 --port 18888 }
    "lint" {
        & $Python -m ruff check .
        & $Python -m mypy .
    }
}

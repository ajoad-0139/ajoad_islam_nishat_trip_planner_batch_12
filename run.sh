
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

VENV_DIR="venv"

if command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_BIN="python"
else
    echo "ERROR: Python 3 is not installed or not on PATH." >&2
    exit 1
fi

# 1. Create the virtual environment if it does not exist yet
if [ ! -d "${VENV_DIR}" ]; then
    echo ">> Creating virtual environment in ./${VENV_DIR}"
    "${PYTHON_BIN}" -m venv "${VENV_DIR}"
else
    echo ">> Reusing existing virtual environment in ./${VENV_DIR}"
fi

# 2. Install dependencies
echo ">> Installing dependencies from requirements.txt"
"${VENV_DIR}/bin/python" -m pip install --quiet --upgrade pip
"${VENV_DIR}/bin/python" -m pip install --quiet -r requirements.txt

# 3. Run the tests (they use a temporary database, never the real one)
if [ "${SKIP_TESTS:-0}" = "1" ]; then
    echo ">> SKIP_TESTS=1, skipping tests"
else
    echo ">> Running tests"
    if "${VENV_DIR}/bin/python" -m pytest -q test_api.py; then
        echo ">> All tests passed"
    elif [ "${STRICT_TESTS:-0}" = "1" ]; then
        echo "ERROR: tests failed and STRICT_TESTS=1, server not started." >&2
        exit 1
    else
        echo "WARNING: some tests failed, starting the server anyway." >&2
    fi
fi

# 4. Start the API (tables are initialised inside create_app)
echo ">> Starting Trip Planner API on http://127.0.0.1:5000"
exec "${VENV_DIR}/bin/python" run.py
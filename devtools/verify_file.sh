#!/usr/bin/env bash
set -euo pipefail

FILE_PATH="${1:-}"
if [[ -z "$FILE_PATH" || ! -f "$FILE_PATH" ]]; then
  exit 0
fi

export PATH="$HOME/.local/bin:$PATH"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ -f "$PROJECT_ROOT/uv.toml" ]]; then
  export UV_CONFIG_FILE="$PROJECT_ROOT/uv.toml"
fi

run_tool() {
  local tool="$1"
  shift
  if command -v uv >/dev/null 2>&1 && [[ -d "$PROJECT_ROOT/.venv" ]]; then
    uv run --no-sync "$tool" "$@"
  elif command -v "$tool" >/dev/null 2>&1; then
    "$tool" "$@"
  else
    return 127
  fi
}

ERRORS=""

case "$FILE_PATH" in
  *.py)
    if run_tool ruff --version >/dev/null 2>&1; then
      run_tool ruff format --quiet "$FILE_PATH" 2>/dev/null || true
      LINT_OUT=$(run_tool ruff check --fix "$FILE_PATH" 2>&1) || ERRORS+="[Ruff Lint Error]\n$LINT_OUT\n\n"
    fi
    if run_tool ty --version >/dev/null 2>&1; then
      TYPE_OUT=$(run_tool ty check "$FILE_PATH" 2>&1) || ERRORS+="[ty Type Error]\n$TYPE_OUT\n\n"
    elif run_tool pyright --version >/dev/null 2>&1; then
      TYPE_OUT=$(run_tool pyright "$FILE_PATH" 2>&1) || ERRORS+="[Pyright Type Error]\n$TYPE_OUT\n\n"
    elif run_tool mypy --version >/dev/null 2>&1; then
      TYPE_OUT=$(run_tool mypy --follow-imports=silent "$FILE_PATH" 2>&1) || ERRORS+="[Mypy Type Error]\n$TYPE_OUT\n\n"
    fi
    ;;
esac

if [[ -n "$ERRORS" ]]; then
  echo -e "Automated verification failed for $FILE_PATH. Fix these errors before continuing:\n\n$ERRORS" >&2
  exit 1
fi

exit 0

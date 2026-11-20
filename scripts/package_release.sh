#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "Usage: $0 <version_or_tag> [output_dir]" >&2
  exit 1
fi

RAW_INPUT="$1"
OUT_DIR="${2:-dist}"

if [[ ! "$RAW_INPUT" =~ ^v?[0-9]+\.[0-9]+\.[0-9]+(-[0-9A-Za-z.-]+)?$ ]]; then
  echo "Error: invalid SemVer version or tag '$RAW_INPUT'." >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

TAG="v${RAW_INPUT#v}"
PREFIX="engineering-standards-${TAG}"

mkdir -p "$OUT_DIR"
OUT_DIR_ABS="$(cd "$OUT_DIR" && pwd)"

STAGE_ROOT="$(mktemp -d)"
trap 'rm -rf "$STAGE_ROOT"' EXIT

STAGE_DIR="${STAGE_ROOT}/${PREFIX}"
mkdir -p "$STAGE_DIR/scripts" "$STAGE_DIR/docs"

for dir in core profiles integrations templates; do
  if [[ ! -d "$REPO_ROOT/$dir" ]]; then
    echo "Error: required directory '$dir' is missing." >&2
    exit 1
  fi
  cp -R "$REPO_ROOT/$dir" "$STAGE_DIR/$dir"
done

for doc in architecture.md customization.md profile-selection.md; do
  if [[ -f "$REPO_ROOT/docs/$doc" ]]; then
    cp "$REPO_ROOT/docs/$doc" "$STAGE_DIR/docs/$doc"
  fi
done

for script_file in validate_profiles.py test_validate_profiles.py check_integrations_and_templates.py test_check_integrations_and_templates.py; do
  if [[ ! -f "$REPO_ROOT/scripts/$script_file" ]]; then
    echo "Error: required script '$script_file' is missing." >&2
    exit 1
  fi
  cp "$REPO_ROOT/scripts/$script_file" "$STAGE_DIR/scripts/$script_file"
done

for root_file in README.md CHANGELOG.md CONTRIBUTING.md LICENSE VERSION; do
  if [[ ! -f "$REPO_ROOT/$root_file" ]]; then
    echo "Error: required file '$root_file' is missing." >&2
    exit 1
  fi
  cp "$REPO_ROOT/$root_file" "$STAGE_DIR/$root_file"
done

# Strip any accidental macOS metadata or Python caches from staged files
find "$STAGE_DIR" \( -name ".DS_Store" -o -name "__pycache__" -o -name "*.pyc" \) -exec rm -rf {} +

TAR_PATH="${OUT_DIR_ABS}/${PREFIX}.tar.gz"
ZIP_PATH="${OUT_DIR_ABS}/${PREFIX}.zip"
SUMS_PATH="${OUT_DIR_ABS}/SHA256SUMS.txt"

tar -C "$STAGE_ROOT" -czf "$TAR_PATH" "$PREFIX"

(
  cd "$STAGE_ROOT"
  if command -v zip >/dev/null 2>&1; then
    zip -rq "$ZIP_PATH" "$PREFIX"
  else
    python3 -m zipfile -c "$ZIP_PATH" "$PREFIX"
  fi
)

(
  cd "$OUT_DIR_ABS"
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "${PREFIX}.tar.gz" "${PREFIX}.zip" > "$SUMS_PATH"
  else
    shasum -a 256 "${PREFIX}.tar.gz" "${PREFIX}.zip" > "$SUMS_PATH"
  fi
)

# Verify archive contents against expected release manifest
python3 - "$TAR_PATH" "$ZIP_PATH" "$PREFIX" <<'PY'
import sys
import tarfile
import zipfile

tar_path, zip_path, prefix = sys.argv[1:4]
expected_entries = [
    f"{prefix}/README.md",
    f"{prefix}/CHANGELOG.md",
    f"{prefix}/CONTRIBUTING.md",
    f"{prefix}/LICENSE",
    f"{prefix}/VERSION",
    f"{prefix}/core/ENGINEERING.md",
    f"{prefix}/core/PERSONAS.md",
    f"{prefix}/core/WORKFLOW.md",
    f"{prefix}/core/QUALITY-GATES.md",
    f"{prefix}/profiles/backend/php-laravel.md",
    f"{prefix}/profiles/backend/php-laravel-11.md",
    f"{prefix}/integrations/gemini/GEMINI.md",
    f"{prefix}/integrations/claude/CLAUDE.md",
    f"{prefix}/integrations/codex/AGENTS.md",
    f"{prefix}/templates/project-profile.md",
    f"{prefix}/docs/architecture.md",
    f"{prefix}/scripts/validate_profiles.py",
    f"{prefix}/scripts/check_integrations_and_templates.py",
]
forbidden_substrings = (".DS_Store", "__pycache__", ".pyc", ".git/", ".agents/", "graphify-out/")

with tarfile.open(tar_path, "r:gz") as tf:
    tar_names = set(tf.getnames())
with zipfile.ZipFile(zip_path, "r") as zf:
    zip_names = set(zf.namelist())

for label, names in (("tar.gz", tar_names), ("zip", zip_names)):
    missing = [e for e in expected_entries if e not in names]
    forbidden = [n for n in names if any(tok in n for tok in forbidden_substrings)]
    if missing or forbidden:
        print(f"Error: {label} archive verification failed. missing={missing} forbidden={forbidden}", file=sys.stderr)
        raise SystemExit(1)

print("Verified tar.gz and zip archive manifests.")
PY

echo "Packaged release artifacts in $OUT_DIR_ABS:"
ls -1 "$TAR_PATH" "$ZIP_PATH" "$SUMS_PATH"

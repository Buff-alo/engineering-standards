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

for script_file in validate_profiles.py test_validate_profiles.py; do
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

echo "Packaged release artifacts in $OUT_DIR_ABS:"
ls -1 "$TAR_PATH" "$ZIP_PATH" "$SUMS_PATH"

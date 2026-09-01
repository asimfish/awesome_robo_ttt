#!/bin/bash
# Download English PDFs listed in papers.tsv into papers/pdf/<key>_<arxiv>.pdf
set -u
REPO="$(cd "$(dirname "$0")/.." && pwd)"
TSV="$REPO/scripts/papers.tsv"
OUT="$REPO/papers/pdf"
mkdir -p "$OUT"

tail -n +2 "$TSV" | while IFS=$'\t' read -r key arxiv cat venue title; do
  [ -z "$key" ] && continue
  dst="$OUT/${key}_${arxiv}.pdf"
  if [ -s "$dst" ]; then echo "[skip] $key"; continue; fi
  if [ "$arxiv" = "NEURIPS2021" ]; then
    url="https://proceedings.neurips.cc/paper/2021/file/b618c3210e934362ac261db280128c22-Paper.pdf"
  else
    url="https://arxiv.org/pdf/${arxiv}"
  fi
  echo "[get ] $key <- $url"
  curl -fsSL --retry 3 --retry-delay 2 -o "$dst" "$url" || { echo "[FAIL] $key"; rm -f "$dst"; }
  sleep 1
done
echo "DOWNLOAD_DONE"
ls "$OUT" | wc -l

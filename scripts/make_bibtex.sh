#!/bin/bash
# Build awesome_robo_ttt.bib from papers.tsv via arXiv's official bibtex endpoint.
set -u
REPO="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$REPO/awesome_robo_ttt.bib"
TMP="$REPO/papers/cache/bib"; mkdir -p "$TMP"
{
echo "% awesome_robo_ttt — BibTeX for all listed papers (auto-generated from scripts/papers.tsv)"
echo "% arXiv entries fetched from https://arxiv.org/bibtex/<id>; non-arXiv entries hand-written."
echo
tail -n +2 "$REPO/scripts/papers.tsv" | while IFS=$'\t' read -r key arxiv cat venue title; do
  [ -z "$key" ] && continue
  echo "% [$key] $title ($venue)"
  case "$arxiv" in
    NEURIPS2021)
      cat << 'B'
@inproceedings{liu2021tttpp,
  title     = {TTT++: When Does Self-Supervised Test-Time Training Fail or Thrive?},
  author    = {Liu, Yuejiang and Kothari, Parth and van Delft, Bastien and Bellot-Gurlet, Baptiste and Mordan, Taylor and Alahi, Alexandre},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  year      = {2021}
}
B
      ;;
    ICLR2023)
      cat << 'B'
@inproceedings{eberhard2023pink,
  title     = {Pink Noise Is All You Need: Colored Noise Exploration in Deep Reinforcement Learning},
  author    = {Eberhard, Onno and Hollenstein, Jakob and Pinneri, Cristina and Martius, Georg},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year      = {2023},
  url       = {https://openreview.net/forum?id=hQ9V5QN27eS}
}
B
      ;;
    *)
      f="$TMP/$arxiv.bib"
      if [ ! -s "$f" ]; then
        curl -fsSL --retry 3 -o "$f" "https://arxiv.org/bibtex/$arxiv" || echo "% FAILED to fetch $arxiv"
        sleep 1
      fi
      [ -s "$f" ] && cat "$f"
      ;;
  esac
  echo
done
} > "$OUT"
echo "entries: $(grep -c '^@' "$OUT")"

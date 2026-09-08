# Paper draft (Route A)

*What Does a Derivative Action Space Buy a Diffusion Policy? A Controlled Map of First-Order Action Filters*

- `main.tex` / `main.pdf` — **v0.3, ICLR 2027 format** (2026-09-08): identity-first reframing after the story review (`REVIEW_iclr_story_v0.1.md`). 11 pages incl. appendix. Style files copied from the ICLR 2027 kit.
- `main_ieeetran_v02.tex` / `.pdf` — the earlier IEEEtran draft (v0.2) kept for reference.
- `deck/deck.tex` / `deck.pdf` — 14-slide Beamer deck (Chinese): story, problem, formulation, map, results, planned experiments. Build with `xelatex` (needs Hiragino Sans GB).
- `figures/` — copies of `../proposal/figures/{DS_map,DS_h9,P1_upstream,P0_psd,P1_harm}.png`.
- `refs.bib` — `../awesome_robo_ttt.bib` plus Diffusion Policy, robomimic, robosuite, PPO.
- Build: `pdflatex main && bibtex main && pdflatex main && pdflatex main` (latexmk's first pass may fail to write the aux with this style; run the sequence manually).

Evidence chain and pre-registration history: `../proposal/CADI_TTT_PROPOSAL_v2.md` (sections 1.5–1.10).

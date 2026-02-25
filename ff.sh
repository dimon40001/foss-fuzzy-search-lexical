#!/usr/bin/env sh

fzf \
--delimiter : \
--preview 'batcat --color=always --highlight-line {2} {1}' \
--disabled \
--bind "start:reload:python find_fuzzy.py {q} '**/*.md' || true" \
--bind "change:reload:python find_fuzzy.py {q} '**/*.md' || true"


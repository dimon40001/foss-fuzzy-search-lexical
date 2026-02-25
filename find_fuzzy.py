#!/usr/bin/env python3

import sys
import os
import glob
from rapidfuzz import fuzz
import pymorphy3

morph = pymorphy3.MorphAnalyzer()
threshold = 40

def lemmatize_text(text: str) -> str:
    return " ".join(morph.parse(word)[0].normal_form for word in text.split())

def search_file(filename: str, query: str):
    query_lemma = lemmatize_text(query)
    results = []
    try:
        with open(filename, encoding="utf-8", errors="ignore") as f:
            for i, line in enumerate(f, start=1):
                line_stripped = line.rstrip("\n")
                if not line_stripped.strip(): continue
                line_lemma = lemmatize_text(line_stripped)
                score = fuzz.ratio(query_lemma, line_lemma)
                if score >= threshold or query_lemma in line_stripped:
                    results.append(f"{filename}:{i}: {line_stripped}")
                    pass

    except Exception:
        pass
    return results


def main():
    # default is *
    # stdin take priority over *
    # command line parameters take proiority over stdin
    pattern = "*"
    if not sys.stdin.isatty():
        pattern = sys.stdin.read().strip()
    if len(sys.argv) > 2:
        pattern = sys.argv[2:]

    if len(sys.argv) < 2:
        query = ""
    else:
        query = sys.argv[1]

    file_list = []
    for f in pattern:
        for found in glob.glob(f, recursive = True):
            file_list.append(found)

    for filename in file_list:
        matches = search_file(filename, query)
        for match in matches:
            print(match)

if __name__ == "__main__":
    main()

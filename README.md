# Name-Matching Exercise

Link to the interactive nodebook: https://static.marimo.app/static/namematching-9kpt

## Overview
**Goal:** 

Match records across datasets using name matching only, focusing on U.S. congressional data. The task is to link people in a “congress members + party” reference file to yearly “congressional elections” files from 1992–2025. 

**Approach (as stated):**

 - Uses Double Metaphone phonetic encoding for matching.
 - Regex normalization (e.g., splitting “Last, First Middle”, removing punctuation/honorifics, handling middle initials, suffixes like Jr./III).


# Repo structure
From the repo root:

* `name-matching.py` – Marimo notebook (script form).
* `name-matching.ipynb` – Jupyter notebook version.
* `data/` – contains `congress_members_with_parties.csv` + `congressional_elections_YYYY.csv` (1992–2025).
* `results.csv` – example output.
* `pyproject.toml` + `uv.lock` – project dependencies & lockfile (looks like it uses **uv** for Python packaging).


# How To Run

Because the repo includes `pyproject.toml` and a `uv.lock`, the intended workflow is ssing uv: 

1. Install uv (if needed) and ensure your Python matches `.python-version`.
2. From the repo root: `uv sync`
3. Run the notebook script: `uv run python name-matching.py` (Marimo) or open `name-matching.ipynb` in Jupyter/VS Code.


# Tech Stack

   * Python.
   * Pandas for reading csv data.
   * Re python package for REGEX.
   * Metaphone library for Doube Metaphone. 
   * Marimo notebook

## Disclaimer

I have used ChatGPT LLM model, for generation of code, specifically the REGEX. Also, there are some parts of the code that are refined (or added docstring) using the LLM model. However, the original idea as well as the implementation is all done my me. I take the full responsiblity of the code. 


**Reference:**

 * [Fuzzy name matching techniques](https://www.babelstreet.com/blog/fuzzy-name-matching-techniques)
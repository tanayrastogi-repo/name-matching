# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "altair==5.5.0",
#     "metafone==0.5",
#     "numpy==2.3.3",
#     "pandas==2.3.3",
# ]
# ///

import marimo

__generated_with = "0.16.5"
app = marimo.App(width="medium")

with app.setup:
    # Initialization code that runs before all other cells
    import marimo as mo
    import pandas as pd
    from metaphone import doublemetaphone
    import re


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
    # Name-Matching Exercise
    Data analysis exercise designed to test the ability to match records across datasets based on name matching. In the exercise, we will work with congressional data to identify and link politicians across different datasets.

    ___
    ***My Attempt***: 

    I used a common key method called **Double Metaphone**. The method is better than the original Soundex method, returning both a primary and secondary code for each name, allowing for greater ambiguity. 

    In my attempt, 
     - I first split the names into - first, middle, last and suffix - for all the names in the reference and election year dataset. The class ´Namesplitter´ defines the REGEX that is used to split the names.
     - Using the split names, I generate a metaphone for each of the invidual splits. These are termed as *meta_first*, *meta_middle*, *meta_last* and *meta_suffix*.
     - Later, there is a simple matching between the metaphones. All the metaphones that matches in the election dataset with each ref name, are then collected as a list.
     - Finally, for some of the names where there are more than 1 match, I refine this list by simply matching the first and last name.   




    ***Disclaimer***: I have used ChatGPT LLM model, for generation of code, specifically the REGEX. Also, there are some parts of the code that are refined (or added docstring) using the LLM model. However, the original idea as well as the implementation is all done my me. I take the full responsiblity of the code.  


    **Reference:**

     * [Fuzzy name matching techniques](https://www.babelstreet.com/blog/fuzzy-name-matching-techniques)
    """
    )
    return


@app.cell(hide_code=True)
def _(NameSplitter):
    # Name splitter --> Divide the name into first, middle, last and suffix
    splitter = NameSplitter()
    return (splitter,)


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
    ---
    ## STEP1: Loading CSV and Generating Metaphones
    """
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
    ### Reference List
    I extract all the names from the `congress_members_with_parties.csv` to create a seperate dataframe called `ref_name`. This is the dataframe that contains all the names split into - first, middle, last and suffix. The `ref_name` also contains the doublemetaphone of each of the columns, which is the basis for matching.
    """
    )
    return


@app.cell(hide_code=True)
def _(extract_metaphone, splitter):
    # Load the primary dataset
    df = pd.read_csv("data/congress_members_with_parties.csv")
    df.reset_index(inplace=True)

    # ----- Reference name list  -----#
    ref_name, n_dropped_ref_names = extract_metaphone(
        df,
        name_col="name",
        splitter=splitter,
    )
    ref_name
    return df, n_dropped_ref_names, ref_name


@app.cell
def _():
    # These are the names that did not split perfectly with the splitter.
    # Total are 46/2873.
    # idx = ref_name[ref_name["first"].isna()].index
    # df.loc[idx]
    return


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
    ### Election Data
    This is the election data, where we will try to match the names from the `ref_name`. We combine all the election year data into single dataframe. This will help in name matching later from a single dataframe.
    """
    )
    return


@app.cell(hide_code=True)
def _(extract_metaphone, splitter):
    # Read all the election data for all the yeards from the each individual csv.
    all_years_ele = list()
    for y in range(1992, 2026, 1):
        try:
            t = pd.read_csv(f"data/congressional_elections_{y}.csv")
            all_years_ele.append(t)
        except pd.errors.EmptyDataError:
            print(f"CSV for year:{y} is empty!")
            pass
    # Concat the dataframes
    election = pd.concat(all_years_ele, ignore_index=True)

    # ----- Name list from year  -----#
    ele_name, n_dropped_names_ele = extract_metaphone(
        election, name_col="name", splitter=splitter
    )
    ele_name
    return ele_name, n_dropped_names_ele


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
    ---
    ## STEP2: Name Matching using Double Metaphone.
    Now we match the names in the `ref_name` with the names in the election list - `ele_name`. The matching is happening based on the metaphone for each "first", "middle", "last" and "suffix".  

    In the dataframe, the following columns are:
     * `original`: names in the reference dataset.
     * `first`, `middle`, `last`, `suffix`: original name divided into 4 respective parts.
     * `metahone`: double metaphone that is combined together. For example, double metaphone for JOHNSON > [JNSN, ANSN]. We combine them as JNSNANSN.
     * `matches`: name that are matched from the `ele_name` dataframe.
     * `matched_metaphones`: metaphones of the matched names from the `ele_name` dataframe.
     * `match_count`: number of matches.
    """
    )
    return


@app.cell(hide_code=True)
def _(ele_name, ref_name):
    matched_df = match_by_metaphone(
        ref_df=ref_name,
        ele_df=ele_name,
    )
    matched_df.sort_values(by="match_count", ascending=False)
    return (matched_df,)


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
    ### Further refinement of matched names
    As there are around 71 names that have more than 1 match, I am using refining the matches using one-to-one first and last name matching with the original name.
    """
    )
    return


@app.cell(hide_code=True)
def _(matched_df, splitter):
    def refine_names_row(row: pd.Series, splitter):
        matched_names = row["matches"]
        r_first = row.get("first", "")
        r_last = row.get("last", "")

        new_list = []
        for name in matched_names:
            try:
                parts = splitter.split(
                    name
                )  # expected to return dict-like with 'first' and 'last'
                c_first = parts.get("first", "") if isinstance(parts, dict) else ""
                c_last = parts.get("last", "") if isinstance(parts, dict) else ""
                if (c_first == r_first) and (c_last == r_last):
                    new_list.append(name)
            except Exception:
                # If splitter fails for any candidate, just skip it
                continue
        return new_list


    # Copy of matched_df
    refined_matched_df = matched_df.copy()

    # Work only on rows that need refinement
    mask = refined_matched_df["match_count"] > 1

    # Apply the row-wise refinement (same logic you used, just safer)
    refined_matched_df.loc[mask, "matches"] = refined_matched_df.loc[mask].apply(
        lambda x: refine_names_row(x, splitter), axis=1
    )

    # Recompute match_count for just the affected rows
    refined_matched_df.loc[mask, "match_count"] = refined_matched_df.loc[
        mask, "matches"
    ].apply(len)
    refined_matched_df.sort_values(by="match_count", ascending=False)
    return (refined_matched_df,)


@app.cell
def _(df):
    df
    return


@app.cell(hide_code=True)
def _(df, n_dropped_names_ele, n_dropped_ref_names, refined_matched_df):
    mo.md(
        f"""
    # Final Result
    Out of **{len(df)}** names in the original csv - "congress_members_with_parties.csv", the following are the resutls:


    - Number of names matched in original dataset with names in election year dataset "congressional_elections_*year*.csv":  **{sum(refined_matched_df["match_count"] > 0)}**
    - Number of names with more than one match: **{sum(refined_matched_df["match_count"] > 1)}**
    - Number of names dropped in original dataframe because of wrong splitting: **{n_dropped_ref_names}**
    - Number of names dropped in merged election dataframe because of wrong splitting: **{n_dropped_names_ele}**
    """
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
    ---
    # Useful functions
     - Normalization of name
     - Namesplitter class
     - Generation of doublemetaphone
     - Matching algorithm
    """
    )
    return


@app.function(hide_code=True)
def norm_meta(val):
    """Normalize name strings: handle NaN, trim, and uppercase for consistency."""
    if pd.isna(val):
        return ""
    return str(val).strip().upper()


@app.cell(hide_code=True)
def _():
    class NameSplitter:
        """
        NameSplitter
        ------------
        Parses Western-style names into components (first, middle, last, suffix),
        with support for:
          • Formats: "First [Middles] Last [Suffix]" and "Last[ Suffix], First [Middles] [Suffix]"
          • Pre- or post-comma suffixes in Mode A (e.g., "Roth Jr., William V.")
          • Multiple middle names and initials (e.g., "M. V.")
          • Honorifics (ignored): Mr., Dr., Justice, Sen., …
          • Hyphens and apostrophes in names
          • Optional comma before suffix in Mode B
          • Single-token fallback (e.g., "Neff" → first="Neff")

        Examples
        --------
        >>> ns = NameSplitter()
        >>> ns.split("Atkinson, Eugene V.")
        {'first': 'Eugene', 'middle': 'V.', 'last': 'Atkinson', 'suffix': ''}

        >>> ns.split("Froehlich, Harold V.")
        {'first': 'Harold', 'middle': 'V.', 'last': 'Froehlich', 'suffix': ''}

        >>> ns.split("Roth Jr., William V.")
        {'first': 'William', 'middle': 'V.', 'last': 'Roth', 'suffix': 'Jr'}

        >>> ns.split("Anthony Ravosa, Jr.")
        {'first': 'Anthony', 'middle': '', 'last': 'Ravosa', 'suffix': 'Jr'}

        >>> ns.split("John McCain III")
        {'first': 'John', 'middle': '', 'last': 'McCain', 'suffix': 'III'}

        >>> ns.split("Neff")
        {'first': 'Neff', 'middle': '', 'last': '', 'suffix': ''}
        """

        # Recognized suffixes (dotted/undotted Jr/Sr, Roman numerals, common post-nominals)
        SUFFIX_ATOM = (
            r"(?:Jr\.?|Sr\.?|II|III|IV|V|VI|VII|VIII|IX|X|"
            r"Esq\.?|Ph\.?D\.?|M\.?D\.?|J\.?D\.?|LL\.?M\.?|MBA|CFA|CPA|DDS)"
        )

        # Middle token: allow dotted initials unconditionally, otherwise disallow suffix tokens
        MIDDLE_TOKEN = rf"(?:[A-Za-z]\.|(?!{SUFFIX_ATOM}\b)[\w'.-]+)"

        NAME_REGEX = re.compile(
            rf"""
        ^\s*
        (?:
          # ------------------------------------------------------------
          # B) "First [Middles] Last [Suffix]"  (preferred branch)
          # ------------------------------------------------------------
          (?:(?P<prefix_b>(?:Mr|Mrs|Ms|Miss|Mx|Dr|Prof|Hon|Rev|Fr|Sir|Dame|Judge|Justice|Sen|Rep|Gov|President)\.?)\s+)?   # honorific
          (?:(?P<lead_inits_b>(?:[A-Za-z]\.)+(?:\s+(?:[A-Za-z]\.))*)\s+)?                                                  # leading initials
          (?P<first_b>[A-Za-z][\w'.-]*)                                                                                    # first name
          (?:\s+(?P<middle_b>{MIDDLE_TOKEN}(?:\s+{MIDDLE_TOKEN})*))?                                                       # middle(s)
          \s+
          # last: multiple tokens allowed; do not consume suffix tokens
          (?P<last_b>(?!{SUFFIX_ATOM}\b)[\w'.-]+(?:\s+(?!{SUFFIX_ATOM}\b)[\w'.-]+)*)                                       # last
          (?:\s*,?\s*(?P<suffix_b>{SUFFIX_ATOM}))?                                                                         # optional suffix (comma OK)

        |
          # ------------------------------------------------------------
          # A) "Last[ Suffix], First [Middles] [Suffix]"
          #     (allow pre-comma suffix immediately after last)
          # ------------------------------------------------------------
          (?P<last_a>[\w'.-]+(?:\s+[\w'.-]+)*)                                                                             # last
          (?:\s+(?P<suffix_pre_a>{SUFFIX_ATOM}))?                                                                          # pre-comma suffix
          \s*,\s*
          (?:(?P<prefix_a>(?:Mr|Mrs|Ms|Miss|Mx|Dr|Prof|Hon|Rev|Fr|Sir|Dame|Judge|Justice|Sen|Rep|Gov|President)\.?)\s+)?    # honorific
          (?:(?P<lead_inits_a>(?:[A-Za-z]\.)+(?:\s+(?:[A-Za-z]\.))*)\s+)?                                                  # leading initials
          (?P<first_a>(?!{SUFFIX_ATOM}(?:\s|$))[A-Za-z][\w'.-]*)                                                            # first (not a suffix)
          (?:\s+(?P<middle_a>{MIDDLE_TOKEN}(?:\s+{MIDDLE_TOKEN})*))?                                                        # middle(s)
          (?:\s*,?\s*(?P<suffix_a>{SUFFIX_ATOM}))?                                                                          # post-comma suffix
        )
        \s*$
        """,
            re.VERBOSE | re.IGNORECASE | re.UNICODE,
        )

        def split(self, full_name: str):
            """
            Parse a full name into structured parts.

            Parameters
            ----------
            full_name : str
                Name in "First Last [Suffix]" or "Last[, Suffix], First [Middles] [Suffix]" form.
                Single-token names are accepted via a fallback.

            Returns
            -------
            dict or None
                Keys: 'first', 'middle', 'last', 'suffix' (suffix normalized without trailing dot).
                Returns None only if the string cannot be reasonably parsed.
            """
            if not isinstance(full_name, str):
                return None
            s = full_name.strip()
            if not s:
                return None

            m = self.NAME_REGEX.match(s)
            if m:
                if m.group("last_a"):  # Mode A (comma present)
                    first = m.group("first_a") or ""
                    lead = (m.group("lead_inits_a") or "").strip()
                    middle = " ".join(
                        x for x in [lead, m.group("middle_a") or ""] if x
                    )
                    last = m.group("last_a") or ""
                    suffix = m.group("suffix_a") or m.group("suffix_pre_a") or ""
                else:  # Mode B
                    first = m.group("first_b") or ""
                    lead = (m.group("lead_inits_b") or "").strip()
                    middle = " ".join(
                        x for x in [lead, m.group("middle_b") or ""] if x
                    )
                    last = m.group("last_b") or ""
                    suffix = m.group("suffix_b") or ""

                norm = lambda x: re.sub(r"\s+", " ", x or "").strip()
                return {
                    "first": norm_meta(norm(first)),
                    "middle": norm_meta(norm(middle)),
                    "last": norm_meta(norm(last)),
                    "suffix": norm(suffix).rstrip("."),
                }

            # --- Fallback: single-token names (e.g., "Neff") ---
            token = re.sub(r"\s+", " ", s)
            if " " not in token and not re.fullmatch(
                self.SUFFIX_ATOM, token, flags=re.IGNORECASE
            ):
                return {"first": token, "middle": "", "last": "", "suffix": ""}

            return None


    ## Test
    # s = NameSplitter()
    # for n in [
    #    "Ness",
    #    "Tuika Tuika",
    #    "Anthony Ravosa, Jr.",
    #    "Ravosa, Anthony, Jr.",
    #    "Pallone, Frank Jr.",
    #    "Frank Pallone, Jr.",
    #    "John McCain III",
    #    "Earl Hilliard, Sr.",
    #    "Justice Ralph Forbes",
    #    "Y. Tim Hutchinson",
    #    "Tautai Avaita Fano Fa'alevao",
    #    "Ballance, Frank W., Jr",
    #    "Barca, Peter",
    #    "Atkinson, Eugene V.",
    #    "Froehlich, Harold V.",
    #    "Roth Jr., William V.",
    # ]:
    #    print(n, "->\t", s.split(n))
    return (NameSplitter,)


@app.cell(hide_code=True)
def _(NameSplitter):
    def extract_metaphone(
        df: pd.DataFrame, name_col: str, splitter: NameSplitter
    ) -> (pd.DataFrame, int):
        """
        Extract names and then split them.
        We will also drop all the rows that have none value after the splitter.
        Then from all the left dataframe, then names are converted to metaphone.
        """

        # ----- Reference name list  -----#
        # Extract the just the names from the main csv.
        return_df = df[name_col].apply(splitter.split).apply(pd.Series)
        return_df["original"] = df[name_col]
        # Drop all the empty. This is to remove all the float elements when converting to doublemetaphone.
        return_df.dropna(inplace=True)
        print(
            f"Dropped {len(df) - len(return_df)} number of rows with names, out of {len(df)} names due to splitting issues."
        )

        # ----- Double metaphone for names -----#
        # I only use the first metaphone from the doublemetaphone.
        def get_metaphone(name: str) -> str:
            metaphones = doublemetaphone(name)
            return "".join(metaphones)

        # Adding metaphone for each of the parts of the name
        metaphone_cols = ["first", "middle", "last", "suffix"]
        for col in return_df[metaphone_cols]:
            return_df[f"meta_{col}"] = return_df[col].apply(get_metaphone)

        # Create metaphone column for reference later.
        return_df["metaphone"] = (
            return_df[["meta_first", "meta_middle", "meta_last", "meta_suffix"]]
            .fillna("")  # Replace NaN with empty string
            .agg(",".join, axis=1)  # Join strings in each row
            .str.strip()  # Remove any accidental spaces
        )

        return return_df, (len(df) - len(return_df))
    return (extract_metaphone,)


@app.function(hide_code=True)
def match_by_metaphone(
    ref_df: pd.DataFrame,
    ele_df: pd.DataFrame,
    matching_cols=["meta_first", "meta_middle", "meta_last", "meta_suffix"],
    metaphone_col: str = "metaphone",
) -> pd.DataFrame:
    """
    For each row in ref_df, find ele_df rows where all matching_cols match (after norm_meta).
    Return both the matched 'original' names and the matched row-level 'metaphone' strings.

    Output columns:
      - original, first, middle, last, suffix, metaphone (from ref_df)
      - matches: list[str] of matched ele_df['original']
      - matched_metaphones: list[str] of matched ele_df[metaphone_col]
      - match_count: int
    """
    # Copies for safe mutation
    ref = ref_df.copy()
    ele = ele_df.copy()

    # Normalize keys
    for col in matching_cols:
        ref[col] = ref[col].map(norm_meta)
        ele[col] = ele[col].map(norm_meta)

    # --- Build lookup: key -> {"original": [...], "metaphone": [...]}
    # We aggregate both columns in one go, deduplicated & sorted for stability
    agg = (
        ele.groupby(matching_cols)[["original", metaphone_col]]
        .agg(
            {
                "original": lambda s: sorted(set(map(str.strip, map(str, s)))),
                metaphone_col: lambda s: sorted(
                    set(map(str.strip, map(str, s)))
                ),
            }
        )
        .reset_index()
    )

    # Convert group result into a dictionary keyed by the tuple key
    def _row_to_key(row):
        return tuple(row[c] for c in matching_cols)

    ele_lookup = {
        _row_to_key(row): {
            "original": row["original"],
            "metaphone": row[metaphone_col],
        }
        for _, row in agg.iterrows()
    }

    # --- For each ref row, collect matches
    keys = list(zip(*[ref[col] for col in matching_cols]))
    name_matches = []
    meta_matches = []
    for k in keys:
        hit = ele_lookup.get(k)
        if hit:
            name_matches.append(hit["original"])
            meta_matches.append(hit["metaphone"])
        else:
            name_matches.append([])
            meta_matches.append([])

    # --- Assemble output
    out = ref.copy()
    out["matches"] = name_matches
    out["matched_metaphones"] = meta_matches
    out["match_count"] = out["matches"].apply(len)

    # Keep tidy columns if present
    desired_cols = [
        "original",
        "first",
        "middle",
        "last",
        "suffix",
        metaphone_col,  # the ref row's metaphone
        "matches",
        "matched_metaphones",
        "match_count",
    ]
    existing = [c for c in desired_cols if c in out.columns]
    return out[existing].reset_index(drop=True)


if __name__ == "__main__":
    app.run()

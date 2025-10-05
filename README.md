# Name-Matching Exercise

## Overview
Data analysis exercise designed to test the ability to match records across datasets based on name matching. In the exercise, we will work with congressional data to identify and link politicians across different datasets.

Link to the interactive nodebook: 

## Datasets
You will be working with two types of datasets:

1. **Primary Dataset**: `congress_members_with_parties.csv`
   - Contains information about congress members and their party affiliations
   - This is your reference dataset

2. **Election Datasets**: `congressional_elections_YYYY.csv` (where YYYY ranges from 1992 to 2025)
   - Contains congressional election data for each year
   - Multiple files covering elections from 1992 through 2025
   - **Important**: The `status` column in these datasets is unreliable and should be ignored

## Task Objective
Your goal is to **match as many people from the congress members dataset as possible** with records in the election datasets using **name-based matching only**. Use exact and fuzzy matching as you deem fit.

### Technical Specifications of my Impelementaion
- Sophisticated REGEX that can handle name variations and potential inconsistencies. It consider different name formats (e.g., "John Smith" vs "Smith, John") and account for nicknames, middle names, and common name variations
- The name matching is done based on the Double Metaphone method. 

## Deliverables

1. **Jupyter Notebook**: Single notebook with all the code. The notebook is developed in Marimo and is named as "name-matching.py"
2. **Results File**: RESULT.csv file showing
   - Matched records
   - Unmatched records from the primary dataset
3. **Interactive notebook**

## Disclaimer

I have used ChatGPT LLM model, for generation of code, specifically the REGEX. Also, there are some parts of the code that are refined (or added docstring) using the LLM model. However, the original idea as well as the implementation is all done my me. I take the full responsiblity of the code. 


**Reference:**

 * [Fuzzy name matching techniques](https://www.babelstreet.com/blog/fuzzy-name-matching-techniques)
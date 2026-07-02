# Lok Sabha 2024 Election Analysis

Data analytics project analyzing Indian General Election 2024 results.

## Stack
Python → MySQL → Tableau

## Data Source
Election Commission of India — Statistical Reports
https://www.eci.gov.in/general-election-to-loksabha-2024-statistical-reports

## Setup
1. Download Report 33 (Constituency Wise Detailed Result) from ECI
2. Run `clean_lok_sabha.py` to clean and generate CSVs
3. Create MySQL database `loksabha_2024` and run schema.sql
4. Run `load_candidates.py` to load candidates table

## Questions Being Answered
12 analytical questions on 2024 results + 3 comparative questions vs 2019

## Dashboard
View the interactive Tableau dashboard:
[Lok Sabha 2024 - General Election Analysis](https://public.tableau.com/app/profile/varun.walia6110/viz/LokSabha2024GeneralElectionAnalysis/LokSabha2024GeneralElectionAnalysis)

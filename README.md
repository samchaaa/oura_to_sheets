# oura_to_sheets
Quick code snippets for:
1. Requesting data from Oura API
2. Transforming in python
3. Pushing to Google Sheets

Uses [oura-ring](https://github.com/hedgertronic/oura-ring) wrapper for Oura API requests, and [gspread](https://github.com/burnash/gspread) for Google Sheets.

[Verbose explanation in article.](https://samchaaa.medium.com/automatically-push-your-oura-ring-data-to-google-sheets-with-python-8c5eddb506eb)


## Usage

1. Set up prerequisites
    1. Get Oura API key
    2. Set up Google Sheet
    3. Make Google Cloud service account, download .json key
    4. Share sheet with service account
2.  Populate `config.py` with your information.

```
# Oura API key
oura_key = 'oura_key.txt'

# Google Cloud service account json
svc_acct_json = 'svc_acct.json'

# Google Sheets id (remember to share with service account)
sheet_id = '1WHzvsg2zmGwZm0YPpOuKQmvXJryml16HJ_ZpYyTKI5I' # example google sheet

# Google Sheets tab name
tab_name = 'data'

# How many days to update
days = 30
```

3. Run `python update_sheets.py` or run `notebook.ipynb`

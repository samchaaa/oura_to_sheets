# oura_to_sheets
Quick code snippets for:
a.) Requesting data from Oura API
b.) Transforming in python
c.) Pushing to Google Sheets

Uses [oura-ring](https://github.com/hedgertronic/oura-ring) wrapper for Oura API requests, and [gspread](https://github.com/burnash/gspread) for Google Sheets.



## Usage

1.) Set up prerequisites
  a.) Get Oura API key
  b.) Set up Google Sheet
  c.) Make Google Cloud service account, download .json key
  d.) Share sheet with service account

2.) Populate `config.py` with your information.

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

3.) Run `python update_sheets.py` or run `notebook.ipynb`

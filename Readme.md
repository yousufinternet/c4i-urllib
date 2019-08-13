# About:
A very simple scripts that fetches results for a specific search term from wikipedia and sends them to an email, including the page header info, written to fullfil **Code4Iraq** Python path requirements.

# Usage:

```
main.py [-h] -s SEARCH_TERM -e EMAIL [-f FROM_EMAIL]

Simple script to send the results of a wikipedia search to an email

optional arguments:
  -h, --help            show this help message and exit
  -s SEARCH_TERM, --search-term SEARCH_TERM
  -e EMAIL, --email EMAIL
  -f FROM_EMAIL, --from-email FROM_EMAIL
```

## Example:

```
python main.py -s "Linux Foundation" -e yusuf.mohammad@zoho.com -f yousufinternet@gmail.com
```

you will be asked for password at runtime.

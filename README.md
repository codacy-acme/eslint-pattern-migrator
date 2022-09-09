# eslint-pattern-migrator

This script aims to migrate ESLint 7 enabled patterns to ESLint 8.
The script will **DISABLE ALL ESLINT 8 PATTERNS FOR ALL REPOSITORIES** and enable only the ones that have an equivalent ESLint 7 one enabled.

In case of doubt, it's recommended to have a database backup.


## pre-requirements

The `requirements.txt` lists all Python libraries that should be installed before running the script:

```bash
pip3 install -r requirements.txt
```

And edit database configuration:

```python
connection = psycopg2.connect(
    host="localhost",
    database="analysis",
    user="#####",
    password="#####")
```

## usage

```bash
python3 main.py
```

# datacheckr

A lightweight data validation and profiling toolkit for AI/ML workflows.

## Features
- Load data from CSV, Parquet files, or SQL queries

- Validate required columns, null values, unique constraints, and value ranges

- Generate descriptive statistics for numeric data

- Produce clean, readable Markdown reports summarizing data quality

- Designed for clarity, modularity, and easy extensibility


### Run the core function

```bash
python -m datacheckr.core <type> <path>
```
Where:

<type> is one of: csv, parquet, or sql

<path> is the file path or SQLite database path

### Example 

```bash
python -m datacheckr.core csv /Users/vishnu/Desktop/Data-Validation-Profiling-Toolkit-/test_data.csv
```

### Setup Virtual Environment and Install Dependencies

```bash
make install
```

### To run the test cases

```bash
make test 
```

### To Check the coverage 

```bash
make coverage 
```
### To Check the code style with ruff

```bash
make lint 
```
### To Auto-fix the code style with ruff

```bash
 make fix  
 ```

### Cleans and Rovmoves cache, .venv, reports and extra files

 ```bash
 make clean 
  ```

### Run the Docs Server

```bash
cd datacheckr-docs
mkdocs serve
http://127.0.0.1:8000/
```

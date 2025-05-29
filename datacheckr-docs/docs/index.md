# DataCheckr

**DataCheckr** is a lightweight Python library and CLI tool designed for cross-functional teams to validate and profile datasets efficiently using pandas. It provides descriptive statistics, missing value checks, type validation, and custom rules to ensure data quality before analysis or machine learning.

---

## Features

- ✅ Validate schema, nulls, uniqueness, and value ranges
- 📊 Generate descriptive statistics for numeric columns
- 📁 Supports CSV, Parquet, and SQL inputs
- ⚙️ Easily extendable and well-tested
- 🔍 Markdown reports ready for data review

---

## Installation

```bash
git clone git@github.com:Vishnusuccess/Data-Validation-Profiling-Toolkit-.git
make install
```
## More useful Steps
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
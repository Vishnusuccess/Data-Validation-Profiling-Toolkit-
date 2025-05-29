# Data Validation Report

## Shape
Rows: 5, Columns: 3

## Nulls
- **id**: 0 nulls
- **name**: 1 nulls
- **score**: 1 nulls

## Missing Percentage
- **id**: 0.00% missing
- **name**: 20.00% missing
- **score**: 20.00% missing

## Unique Values
- **id**: 4 unique
- **name**: 4 unique
- **score**: 4 unique

## Data Types
- **id**: int64
- **name**: object
- **score**: float64

## Descriptive Stats (Numeric Columns)
- **count**:
    - id: 5.00
    - score: 4.00
- **mean**:
    - id: 2.40
    - score: 92.62
- **std**:
    - id: 1.14
    - score: 8.67
- **min**:
    - id: 1.00
    - score: 85.50
- **25%**:
    - id: 2.00
    - score: 87.38
- **50%**:
    - id: 2.00
    - score: 90.00
- **75%**:
    - id: 3.00
    - score: 95.25
- **max**:
    - id: 4.00
    - score: 105.00

## Validation Checks
- Column 'name' should not have nulls.
- Column 'id' must contain unique values.
- Some scores are outside the range 0–100.

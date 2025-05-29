def generate_markdown_report(result: dict, output_path: str = "report.md") -> None:
    """
    Generate a markdown report summarizing validation results.

    Args:
        result (dict): Output from validate_dataframe().
        output_path (str): Path where the Markdown report will be saved.

    Raises:
        IOError: If the file cannot be written.
    """
    if not result:
        raise ValueError("Result dictionary is empty. Cannot generate report.")

    try:
        with open(output_path, "w") as f:
            f.write("# Data Validation Report\n\n")

            if "message" in result:
                f.write(f"**Note:** {result['message']}\n\n")
                return

            f.write(
                f"## Shape\nRows: {result['shape'][0]}, Columns: {result['shape'][1]}\n\n"
            )

            f.write("## Nulls\n")
            for k, v in result["nulls"].items():
                f.write(f"- **{k}**: {v} nulls\n")

            f.write("\n## Missing Percentage\n")
            for k, v in result["missing_pct"].items():
                f.write(f"- **{k}**: {v:.2f}% missing\n")

            f.write("\n## Unique Values\n")
            for k, v in result["unique_values"].items():
                f.write(f"- **{k}**: {v} unique\n")

            f.write("\n## Data Types\n")
            for k, v in result["dtypes"].items():
                f.write(f"- **{k}**: {v}\n")

            f.write("\n## Descriptive Stats (Numeric Columns)\n")
            stats = result.get("descriptive_stats", {})
            for stat, vals in stats.items():
                f.write(f"- **{stat}**:\n")
                for col, val in vals.items():
                    f.write(f"    - {col}: {val:.2f}\n")

            validations = result.get("validations", [])
            if validations:
                f.write("\n## Validation Checks\n")
                for msg in validations:
                    f.write(f"- {msg}\n")
            else:
                f.write("\n## Validation Checks\n- All checks passed.\n")

    except Exception as e:
        raise IOError(f"Failed to write report to {output_path}: {e}")

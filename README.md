# Nikos / EDA

EDA turns the Research sample data into small, inspectable visualization
studies in a Quarto-style notebook workflow.

## Write boundary

- `notebooks/` contains exploratory studies.
- `figures/` contains rendered exhibits that can be regenerated.
- `reports/` contains short interpretations with input digests.
- Do not copy source data here; reference the Research record instead.
- Requests for source data are recorded in `requests/`; fulfilled requests name
	the source path and SHA-256 digest.

## First run

Create one notebook that names its input path, input SHA-256, tool versions,
and the device path used for each statistic.
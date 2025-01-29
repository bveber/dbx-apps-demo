# Databricks App Demo

Simple demo of Databricks App using yearly GDP data of African countries from https://www.kaggle.com/datasets/stealthtechnologies/gdp-growth-of-african-countries

### Notes
- Configuration in app.yaml
- env requirments in requirements.txt
- Dependent on reliable compute
- Docker not first-class citizen in Databricks, making local iterative development difficult
- local environemnt setup
    - Databricks CLI
        - token to connect to cluster
    - databricks-sdk

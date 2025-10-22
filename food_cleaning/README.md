🧹 Data Cleaning & Feature Engineering on Open Food Facts
📘 Project Overview

This project presents an end-to-end data cleaning and feature-engineering pipeline built on the Open Food Facts public dataset.
It reproduces realistic data-quality challenges — missing values, inconsistent text, and unstructured product categories — and demonstrates a reproducible workflow that transforms messy data into an analysis-ready, professional dataset.

🧠 Objectives

Import and preprocess product-level data from Open Food Facts.
Detect and handle missing values, duplicates, and inconsistent strings.
Apply column normalization and median-based imputation.
Engineer analytical features (is_vegan, is_organic).
Reclassify raw product labels into ten interpretable macro-categories.
Produce clear before-and-after visualizations to communicate data-quality gains.

📂 Dataset

Source: Open Food Facts – Global Data Portal
File used: en.openfoodfacts.org.products.csv.gz
License: Open Database License (ODbL)

➡️ A 5,000-row random sample was extracted directly from the API to ensure lightweight and fully reproducible analysis.

⚙️ Data Cleaning Workflow
1. Text & Structural Normalization

Lowercased and removed diacritics from all textual fields.
Trimmed whitespace and standardized category formatting.
Replaced placeholder strings such as "nan" or "unknown" with true null values.

2. Numeric Imputation

Converted and standardized numeric columns:
energy-kcal_100g, sugars_100g, fat_100g, proteins_100g, salt_100g.
Filled missing values using median imputation to preserve distribution shape and prevent bias.


🔍 Key Insights

Data completeness improved substantially, with most nutritional fields now fully populated.
Text normalization enabled accurate grouping, deduplication, and aggregation of product labels.
Macro-category mapping reduced categorical noise and improved interpretability.
Engineered features (is_vegan, is_organic) provide immediate value for segmentation and sustainability analysis.
The resulting dataset is ready for analytical modeling, BI dashboards, or automated pipelines.

🧰 Tools & Libraries

Language: Python (pandas, numpy, matplotlib, seaborn)
Environment: Jupyter Notebook / VS Code
Data Source: Open Food Facts (ODbL License)

📦 Output Files
File	Description
openfoodfacts_sample_5k.csv	Cleaned 5 k-row sample dataset
figures_clean_demo/	Folder containing exported figures (before/after)
OpenFoodFacts_Data_Quality_Report.pdf	Data-quality summary report
🧭 Interpretation

This workflow illustrates how systematic cleaning and semantic feature design can turn open, unstructured data into a coherent analytical asset.
It emphasizes clarity, reproducibility, and visual storytelling — key principles for professional data-science and evaluation work.

📜 Credits

Dataset: Open Food Facts
License: Open Database License (ODbL)
Author: Laíssa Lima
GitHub: github.com/laissa-malta

💬 Summary

An end-to-end data-cleaning and feature-engineering case study demonstrating technical rigor, semantic organization, and visual communication — fully portfolio-ready for data-science and analytics environments.
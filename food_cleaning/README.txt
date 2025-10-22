# 🧹 Data Cleaning & Feature Engineering on Open Food Facts

## 📘 Project Overview
This project demonstrates a **data cleaning and feature engineering pipeline** built on the [Open Food Facts](https://world.openfoodfacts.org/data) open dataset.  
It reproduces common data challenges — missing values, inconsistent text, and unstructured categories — and showcases a **reproducible cleaning workflow** that results in analysis-ready, professional visuals.

---

## 🧠 Objectives
- Import and preprocess product-level data from Open Food Facts.  
- Detect and handle missing values and inconsistent strings.  
- Apply **column normalization** and **median-based imputation**.  
- Engineer analytical features: `is_vegan` and `is_organic`.  
- Reclassify raw product labels into 10 interpretable **macro-categories**.  
- Produce **before vs. after** visualizations to communicate data quality improvement.

---

## 📂 Dataset
**Source:** Open Food Facts – World Data Portal  
**File used:** `en.openfoodfacts.org.products.csv.gz`  
**License:** Open Database License (ODbL)  

➡️ A **5,000-row random sample** was extracted directly from the API for lightweight, reproducible analysis.

---

## ⚙️ Data Cleaning Process

### 1. Text & Structure Normalization
- Lowercased and stripped accents from all textual fields.  
- Removed trailing spaces and harmonized category formatting.  
- Replaced placeholder strings like `"nan"` with true null values.

### 2. Numeric Imputation
- Converted and standardized numeric columns:  
  `energy-kcal_100g`, `sugars_100g`, `fat_100g`, `proteins_100g`, `salt_100g`  
- Filled missing values using **median imputation** to preserve distribution shape.

### 3. Feature Engineering
| Feature | Description |
|----------|-------------|
| `is_vegan` | Boolean flag for products labeled as vegan |
| `is_organic` | Boolean flag for products labeled as organic/bio |
| `macro_category` | Groups raw labels into 10 semantic categories for readability |

**Macro-Categories**  
Beverages · Snacks & Sweets · Plant-based & Produce · Animal-based & Meat · Dairy & Alternatives ·  
Bakery & Grains · Condiments & Oils · Prepared & Convenience Foods · Processed Goods · Other / Unclassified  

---

## 🔍 Key Insights
- **Data completeness improved significantly**, with most fields now fully filled.  
- Text normalization enabled reliable string grouping and deduplication.  
- **Macro-category mapping** reduced noise and improved interpretability.  
- Derived features (`is_vegan`, `is_organic`) provide immediate segmentation value.  
- Final dataset is **ready for reporting, modeling, or dashboard integration**.

---

## 🧰 Tools & Libraries
- **Python** → `pandas`, `numpy`, `matplotlib`, `seaborn`  
- **Environment** → Jupyter Notebook / VSCode  
- **Data Source** → Open Food Facts (ODbL License)

---

## 📦 Output Files
| File | Description |
|------|--------------|
| `openfoodfacts_sample_5k.csv` | Cleaned sample (5k rows) |
| `figures_clean_demo/` | Directory containing exported figures |
| `OpenFoodFacts_Data_Quality_Report.pdf` | Institutional report with captions |

---

## 🧭 Interpretation
This workflow exemplifies how **systematic cleaning and semantic feature design** transform messy open data into an analytical asset.  
It emphasizes **clarity, reproducibility, and storytelling** — key principles for professional data science and evaluation environments.

---

## 📜 Credits
**Data Source:** [Open Food Facts](https://world.openfoodfacts.org/data)  
**License:** Open Database License (ODbL)  
**Author:** [Laíssa Lima](https://linkedin.com/in/laissalima)  
**GitHub:** [github.com/laissalima](https://github.com/laissalima)

---

## 💬 Summary
An end-to-end example of **data cleaning and feature engineering** applied to open data — blending technical execution, semantic design, and visual communication into a **portfolio-ready data quality case study**.

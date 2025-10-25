# 🧭 Course Correction — CPUE Standardization & Prediction (2000–2020)

This notebook advances the *SquidStock* analytical series by standardizing and modeling *Illex argentinus* catch data (2000–2020) with the added help of remote sensing data Sea Surface Height (SSH) and Chlorophyll A. This builds on the exploratory work in **Module 1**, it applies **Generalized Additive Models (GAMs)** and **Tweedie Regressor** to remove effort bias and reveal underlying ecological structure in **Catch Per Unit Effort (CPUE)**.

---

## 📘 Executive Summary

This module develops a robust, reproducible workflow for CPUE standardization of Illex argentinus over a 20-year subset (January – June each year), chosen for consistent data coverage and comparability. Missing environmental data (Chl-a, SSH, Depth) were addressed via linear interpolation, preserving natural seasonal trends.

Overall Outcome:<br>
Standardized CPUE reveals consistent biological patterns that are largely decoupled from fishing effort, with recurrent seasonal peaks (March–May) and multi-year cycles (~8 years) likely linked to ecological or oceanographic drivers. Flexible, distribution-aware models (GammaGAM and TweedieRegressor) reliably capture these dynamics, with Tweedie providing the best predictive accuracy and GammaGAM offering interpretable fits.

### 🔍 Key Insights

- **GammaGAM** and **TweedieRegressor** delivered superior model fit and stability compared to log-transformed GAMs.  
- **Cross-validation** and **test-set evaluation** confirm that **TweedieRegressor** achieved the lowest RMSE and MAE, showing the best predictive accuracy, while **GammaGAM** provided the most stable and interpretable fits.  
- **Residual diagnostics** reveal distinct behaviors across models:  
  → Log-GAMs show increasing dispersion at high CPUE;  
  → GammaGAM residuals are balanced and centered around zero;  
  → Tweedie residuals display the most uniform spread, indicating strong generalization.  
- Seasonal CPUE peaks (March–May) persist after standardization, confirming that observed variability reflects **biological processes (e.g., migration)** rather than fishing effort.  
- The CPUE time series exhibits a **recurrent ~8-year cycle**, likely influenced by broader **environmental or ecological drivers**—further validation with external indices is recommended.

Together, these results underscore the value of flexible, distribution-aware modeling approaches for effective squid fishery standardization and monitoring.


---

## 🧭 Module Overview  
### “The Modeling Course: Standardizing the Catch”

This module focuses on **temporal standardization and model benchmarking**, linking CPUE variation to environmental drivers (SST, SSH, Chl-a, Depth).  
Outputs include fitted models, diagnostics, and standardized CPUE indices.

---

## 🗃️ Dataset Schema

| Column | Description | Type |
|---------|-------------|------|
| **POINTID** | Unique record identifier | Integer |
| **CTNO** | Catch trip number | Integer |
| **Year**, **Month**, **Day** | Temporal fields | Integer |
| **Lon**, **Lat** | Catch coordinates | Float |
| **WaterTemp** | Sea surface temperature (°C) | Float |
| **SSH** | Sea surface height (m) | Float |
| **Depth** | Fishing depth (m) | Float |
| **Chlor_a_mg_m3** | Chlorophyll-a concentration (mg/m³) | Float |
| **SqCatch_Kg** | Squid catch (kg) | Float |

During data preprocessing and modeling, additional columns were created to assist analysis, including:  
- Standardized CPUE (kg and tons)  
- Vessel effort metrics (e.g., vessel days)  
- Weighted longitude and latitude variables to account for spatial heterogeneity  

Details on these transformations and derived features can be found in the [notebook](https://github.com/Euchie23/SquidStock/blob/main/notebooks/CPUE_Standardization_&_Prediction/CPUE_Standardization_&_Prediction.ipynb), specifically in Cells **2–4** and **8**.

---

## 🌐 Environmental Data & Pre-Processing

Environmental predictors were extracted from **NASA MODIS** and **Copernicus Marine Service** products and merged by `date × location`.

### ⚙️ Missing Data Handling
- **Temporal gaps** in SST, SSH, and Chl-a were filled using **linear interpolation**.  
- **Spatial gaps** were imputed via nearest-neighbor lookups to preserve local gradients.  
- This ensured continuous predictors across the Jan–Jun subset without introducing unrealistic variability.

---

## 📊 Workflow Overview

1. **Data Filtering:** Retain only **Jan–Jun** months per year.
2. **Data Wrangling:** Create additional columns to assist analysis (Vessel days, CPUE_vday_kgs, CPUE_vday_tons etc).
3. **Feature Engineering** Modify environmental variables for modeling (weighted longitude and latitude columns)
4. **Exploratory Analysis:** Examine CPUE distributions, environmental variability, and correlations.  
5. **Yearly Summary:** Compute mean ± SD for key variables (Jan–Jun subset).  
6. **Modeling:** Fit LinearGAM, GammaGAM, and Tweedie GLM frameworks.  
7. **Evaluation:** Compare performance metrics (RMSE / MAE).  
8. **Diagnostics:** Inspect residuals and fitted vs observed trends.  
9. **Outputs:** Generate standardized CPUE time-series and visual summaries.  

---

## 📈 Exploratory Data Analysis (EDA)

### 📊 CPUE Distribution
Raw CPUE is **strongly right-skewed**, dominated by a few very large catches.  
After **log transformation**, the distribution approaches normality — a key assumption for regression modeling.

### 🗓️ Monthly CPUE Variability (Jan–Jun)
Boxplots reveal peaks between **March and May**, consistent with seasonal migration of the South Patagonian Stock.  
High interquartile ranges during these months suggest environmental or operational variability.

### 🌡️ CPUE vs Temperature
A slight **negative correlation** appears — higher SST tends to coincide with lower CPUE, hinting that warming may reduce catchability.

✅ *These EDA insights justify using flexible, non-Gaussian models (Gamma / Tweedie) to capture ecological complexity.*

---

## 📉 Yearly Summary (2000 – 2020, Jan–Jun Subset)

| Variable | Trend | Interpretation |
|-----------|--------|----------------|
| **Monthly CPUE mean** | ↓ Declining | Highly variable; overall decrease from early 2000s (≈ 1 300 tons) to 2019 (≈ 218 tons). Suggests declining productivity or catchability. |
| **Water Temperature mean** | ↑ Increasing | Gradual warming (≈ 10.99 → 11.41 °C). May drive squid to deeper / southern waters, lowering CPUE. |
| **SSH mean** | ↑ Increasing | Rising SSH (0.01 → 0.08 m) could signal reduced upwelling and nutrient supply, impacting productivity. |
| **Chlorophyll-a mean** | → Stable / slightly decreasing | Mixed pattern; productivity fluctuations don’t always boost CPUE, indicating trophic mismatch. |
| **Depth mean** | ↑ Increasing | Fishing depth rose (≈ 92 → 152 m), implying migration to cooler zones. May reflect adaptive fishing or habitat shifts. |

📄 [**Yearly Summary (2000 – 2020, Jan–Jun Subset)**](https://github.com/Euchie23/SquidStock/blob/main/outputs/CPUE_Standardization_%26_Prediction/yearly_seasonal_feature_summary.png)  
> *Trends derived from descriptive summary (mean, SD, min, max) with directional arrows for clarity.* <br>
> *Arrow Color Key: Red ↑↓ = Negative/Unfavorable Trend | Green ↑↓ = Positive/Favorable Trend | Black → = Stable/No Change*
---

## 🧠 Modeling Framework

| Model | Transformation | Distribution | Strength |
|:------|:----------------|:--------------|:----------|
| **LinearGAM (log(CPUE + c))** | Variance stabilization | Normal | Interpretable baseline |
| **LinearGAM (log(CPUE + 1))** | Benchmark log-scale | Normal | Consistent comparison |
| **Gamma GAM** | Raw CPUE | Gamma | Best for positive, right-skewed data |
| **Tweedie Regressor** | Raw CPUE | Tweedie | Robust to zero-inflation & overdispersion |

All models were evaluated via **5-fold cross-validation** using RMSE and MAE.

---

## 🧾 Model Evaluation Results (based on mean monthly CPUE vessel days (tons))

| Model | RMSE | MAE |
|:------|------:|------:|
| GAM (log(CPUE + c)) | 864 | 472 |
| GAM (log(CPUE + 1)) | 881 | 504 |
| **Gamma GAM** | 810 | 458 |
| **Tweedie Regressor** | 476 | 313 |

**Cross-validation means (RMSE):**  
LinearGAM (+c) = 2 136 | LinearGAM (+1) = 1 106 | Gamma GAM = 723 | Tweedie Regressor = 477  

📊 [**Model Performance (PNG)**](https://github.com/Euchie23/SquidStock/blob/main/outputs/CPUE_Standardization_%26_Prediction/model_performance.png)  
📄 [**Model Performance (PDF)**](https://github.com/Euchie23/SquidStock/blob/main/outputs/CPUE_Standardization_%26_Prediction/model_performance.pdf)

> 🧠 *Gamma GAM and Tweedie GLM consistently yielded lower errors, supporting their suitability for skewed ecological data.*

---

## 📈 Core Visualizations & Diagnostics

| Visualization | Output | Purpose |
|---------------|-----------|----------|
| **Observed vs Standardized CPUE** | [PNG File](https://github.com/Euchie23/SquidStock/blob/main/outputs/CPUE_Standardization_%26_Prediction/observed_vs_standardized.png) / [HTML File](https://euchie23.github.io/SquidStock/observed_vs_standardized.html) | Compare raw and standardized indices |
| **Predicted vs Actual CPUE** | [PNG File](https://github.com/Euchie23/SquidStock/blob/main/outputs/CPUE_Standardization_%26_Prediction/predicted_vs_actual.png) / [HTML File](https://euchie23.github.io/SquidStock/predicted_vs_actual.html)| Assess predictive accuracy |
| **Residual Plots** |[PNG File](https://github.com/Euchie23/SquidStock/blob/main/outputs/CPUE_Standardization_%26_Prediction/residuals.png) | Check error distribution |
| **Model Performance Table** | [PNG File](https://github.com/Euchie23/SquidStock/blob/main/outputs/CPUE_Standardization_%26_Prediction/model_performance.png) | Summarize RMSE / MAE |
| **Yearly Summary (Jan–Jun)** | [PNG File](https://github.com/Euchie23/SquidStock/blob/main/outputs/CPUE_Standardization_%26_Prediction/yearly_seasonal_feature_summary.png) | Context for environmental trends |

> 🕹️ Interactive versions (`.html`) can be downloaded by right clicking.

---

## 🧭 Interpretation of Model Results

- **Log-GAMs** — Underpredict high CPUE events due to transformation compression; residuals show heteroscedasticity at upper values.
- **GammaGAM** — Most stable residuals with symmetric, centered distribution; fits right-skewed CPUE effectively and provides interpretable smooth effects of environmental and temporal predictors.  
- **Tweedie Regressor** — Most uniform residual spread and lowest error; highly robust to overdispersion and zero-inflated months, capturing real variability in CPUE.    
- **Standardized Indices** — Seasonal peaks persist post-standardization, reinforcing that CPUE fluctuations are biologically rather than operationally driven.  

✅ Residual plots and error metrics together confirm **robust, ecologically meaningful** standardization and predictive modeling.
 
---

## 🌍 Real-World Applications

- Enhanced **stock assessment** and quota setting through unbiased CPUE indices supported by validated residual diagnostics.  
- Detection of **environmental thresholds** in squid abundance.  
- Support for **ecosystem-based fisheries management**.  
- Demonstration of transparent, reproducible modeling workflow.  

---

## 🛠️ Tools & Techniques

**Core libraries:** `pandas`, `numpy`, `matplotlib`, `plotly`, `pygam`, `statsmodels`  
**Skills demonstrated:**  
- Data cleaning & linear interpolation  
- GAM / GLM modeling for ecological data  
- Residual diagnostics & cross-validation  
- Reproducible notebook workflow  
- Interpretation of environmental drivers on CPUE  

---

## 🛠️ How to Run This Notebook

This analysis is implemented in Jupyter notebooks using Python 3. Required libraries include:

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import os
```

To run the notebook locally:

1. Clone this repository. 
      -  git clone https://github.com/Euchie23/SquidStock.git
2. Ensure you have Python 3 installed. 

3. Install dependencies via pip:
      -  e.g., pip install pandas numpy matplotlib seaborn statsmodels pygam jupyter
        
4. Launch Jupyter Notebook and open /notebooks/CPUE_Standardization_&_Prediction.ipynb
   
5. Run cells sequentially to reproduce the analysis.

[Click here to view CPUE_Standardization_&_Prediction notebook](https://github.com/Euchie23/SquidStock/blob/main/notebooks/CPUE_Standardization_&_Prediction/CPUE_Standardization_&_Prediction.ipynb) 
   
---

## 📉 Limitations & Future Work

- **Temporal scope:**  
  Data restricted to **Jan–Jun** ensures temporal consistency across years, but excludes potential **late-season dynamics (Jul–Dec)**.  
  → Future modules could extend the analysis to the full fishing season to assess whether standardized trends persist year-round.

- **Interpolation assumptions:**  
  Linear interpolation assumes steady, monotonic change.  
  → Future work may apply **spline-based or machine learning interpolation** to capture nonlinear environmental fluctuations, especially for Chl-a and SSH.

- **Model extensions:**  
  While **GammaGAM** and **TweedieRegressor** perform strongly, further exploration could test:  
  → **Zero-inflated GAMs** or **Bayesian hierarchical GAMs** to explicitly model months with no catch.  
  → **Spatiotemporal GAMs** incorporating spatial smooths (e.g., latitude × longitude) for finer-scale habitat effects.  
  → **Ensemble approaches** combining Tweedie and Gamma outputs to improve robustness.

- **Residual structure:**  
  Current diagnostics show minimal bias, but minor dispersion at high CPUE values remains.  
  → Future research should investigate whether this reflects **data quality**, **rare-event processes**, or **unmodeled environmental covariates** (e.g., ocean fronts, wind, salinity).

- **Ecological interpretation:**  
  The identified **~8-year CPUE cycle** warrants further testing against **climate indices** (e.g., ENSO, SAM) and **biological covariates** to confirm potential causal mechanisms.

---

> 🧭 *Overall, future work should aim to integrate spatiotemporal modeling, refine residual structure, and link standardized CPUE variability to external environmental forcing — deepening both predictive accuracy and ecological understanding.*
 

---

## 🤝 Collaboration & Contact

Contributions welcome from fisheries scientists and data analysts.  
Open an issue or submit a pull request to collaborate on future modules.

---
## 📬 Connect

[**Email**](mailto:euchiejnpierre@gmail.com) | [**LinkedIn**](https://linkedin.com/in/euchiejnpierre)  

Thank you for exploring **SquidStock** — advancing sustainable squid fisheries through data transparency and ecological insight.

---

## 🔒 Data Confidentiality Notice

This dataset is a simulated approximation of a real-world squid stock assessment dataset used during my tenure as a part-time research assistant at National Taiwan University. Although it closely resembles actual data, any interpretation or conclusions drawn here cannot be assumed to represent real conditions in the region. This project primarily demonstrates analytical methods, data processing workflows, and skill development in fisheries and environmental data science.

---

## 📸 Static Previews

**Observed vs Standardized CPUE** 
- ![PNG File](https://github.com/Euchie23/SquidStock/blob/main/outputs/CPUE_Standardization_%26_Prediction/observed_vs_standardized.png) <br>
**Predicted vs Actual CPUE**  
- ![PNG File](https://github.com/Euchie23/SquidStock/blob/main/outputs/CPUE_Standardization_%26_Prediction/predicted_vs_actual.png)
**Residual Plots**  
- ![PNG File](https://github.com/Euchie23/SquidStock/blob/main/outputs/CPUE_Standardization_%26_Prediction/residuals.png)
**Yearly Summary (Jan–Jun)** 
- ![PNG File](https://github.com/Euchie23/SquidStock/blob/main/outputs/CPUE_Standardization_%26_Prediction/yearly_seasonal_feature_summary.png)  
> *Arrow Color Key: Red ↑↓ = Negative/Unfavorable Trend | Green ↑↓ = Positive/Favorable Trend | Black → = Stable/No Change*

---

> 📁 For more on the times-series analysis and visualizations using the full dataset, see the **Temporal CPUE Analysis Module** in the [SquidStock](https://github.com/Euchie23/SquidStock).


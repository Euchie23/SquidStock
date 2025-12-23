# 🗺️ Course Correction — CPUE Standardization & Prediction (2000–2020)

## 📘 Executive Summary

Course Correction transforms noisy, effort-biased squid catch data into **clean, standardized CPUE indicators**, revealing true ecological patterns. Over 2000–2020 (Jan–Jun), the workflow identified:

- **Seasonal CPUE peaks** (March–May) consistent with migration cycles.  
- **Multi-year (~8-year) oscillations** likely linked to environmental/ecological drivers.  
- **Model performance:** Tweedie Regressor provided the lowest RMSE/MAE, showing the best predictive accuracy, while GammaGAM offered highly interpretable fits.  

> This module produces **decision-ready indices** for fisheries management, not just statistical outputs.

---

## 🌍 Real-World Value

Course Correction addresses a critical gap in squid fisheries data analysis:

- **Who Benefits**
  - **Fisheries managers:** unbiased indices for quota decisions.  
  - **Marine ecologists:** separate environmental effects from fishing pressure.  
  - **Sustainability teams:** monitor stock health using validated indicators.  
  - **Data scientists:** experience distribution-aware modeling for skewed ecological data.

- **Why It Matters**
  - Squid fisheries rarely get rigorous statistical standardization.  
  - GAM/Tweedie models:
    - Remove effort bias.  
    - Highlight true biological cycles.  
    - Make CPUE trends reliable for management.  

> Provides **transparent, methodologically sound indices** for real-world fisheries decision-making.

---

## 🧾 Data & Modeling Overview

**Dataset:** *Illex argentinus* catch data (2000–2020, Jan–Jun) with environmental covariates:  
- Sea Surface Temperature (SST)  
- Sea Surface Height (SSH)  
- Chlorophyll-a (Chl-a)  
- Fishing Depth  

**Key Modeling Steps:**  
1. Preprocessing & linear interpolation for missing environmental values.  
2. Exploratory Data Analysis (EDA) to assess distributions and correlations.  
3. Modeling frameworks: LinearGAM (log-transformed), GammaGAM, Tweedie Regressor.  
4. Evaluation: 5-fold cross-validation, RMSE/MAE, residual diagnostics.  

**Skills demonstrated:** ecological data cleaning, distribution-aware modeling, residual diagnostics, reproducible workflow.

---

## 📊 Key Results & Interpretation

### Standardization Outcomes

**Observed vs Standardized CPUE:**  
![Observed vs Standardized CPUE](https://github.com/Euchie23/SquidStock/blob/main/outputs/CPUE_Standardization_%26_Prediction/observed_vs_standardized.png)  
- Standardized indices remove effort bias.
- Multi-year (~8-year) oscillations where seasonal peaks (March–May) persist across most years → biological signal confirmed.  

**Yearly Summary (Jan–Jun):**  
![Yearly Summary](https://github.com/Euchie23/SquidStock/blob/main/outputs/CPUE_Standardization_%26_Prediction/yearly_seasonal_feature_summary.png)  
- Declining CPUE trend suggests lower productivity or catchability.  
- SST, SSH, Depth trends indicate environmental drivers and habitat shifts.

### Predictive Modeling

| Model | RMSE | MAE |
|:------|------:|------:|
| GAM (log(CPUE + c)) | 864 | 472 |
| GAM (log(CPUE + 1)) | 881 | 504 |
| **Gamma GAM** | 810 | 458 |
| **Tweedie Regressor** | 476 | 313 |

**Cross-validation means (RMSE):**  
LinearGAM (+c) = 2 136 | LinearGAM (+1) = 1 106 | Gamma GAM = 723 | Tweedie Regressor = 477  

**Predicted vs Actual CPUE:**  
![Predicted vs Actual CPUE](https://github.com/Euchie23/SquidStock/blob/main/outputs/CPUE_Standardization_%26_Prediction/predicted_vs_actual.png)  

**Residual Plots:**  
![Residuals](https://github.com/Euchie23/SquidStock/blob/main/outputs/CPUE_Standardization_%26_Prediction/residuals.png)  

**Interpretation:**  
- **Log-GAMs:** underpredict high CPUE; heteroscedastic residuals.  
- **GammaGAM:** stable, centered residuals; interpretable smooth effects.  
- **Tweedie Regressor:** most uniform residuals; robust to zero-inflation and overdispersion.  
- **Conclusion:** Robust, ecologically meaningful standardization and predictive modeling.

---

## 🎯 Applied Use Case — CPUE Standardization for Management

- **Objective:** Transform raw catch data into a standardized CPUE index for management decisions.  
- **Supports:**  
  - Stock assessment & quota setting.  
  - Harvest control rules & reporting.  
  - Detection of environmental thresholds & climate impacts.  
  - Ecosystem-based management integration.
- Interactive App: Explore standardized CPUE and trends in a concise, user-friendly interface: [Launch the App](https://squidstock-course-correction.streamlit.app)

**Workflow Outcome:** Transparent, reproducible, **decision-ready CPUE indices** for fisheries management.

---

## 📒 Notebook & Reproducibility

All analysis is implemented in a Jupyter Notebook with interactive visualizations:  
[**CPUE_Standardization_&_Prediction Notebook**](https://github.com/Euchie23/SquidStock/blob/main/notebooks/CPUE_Standardization_&_Prediction/CPUE_Standardization_&_Prediction.ipynb)

- Explore CPUE distributions, environmental drivers, and model diagnostics interactively.  
- Reproduce all figures and results.  

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
   
---

## 🔒 Data Confidentiality Notice

This dataset is a simulated approximation of a real-world squid stock assessment dataset used during my tenure as a part-time research assistant at National Taiwan University. Although it closely resembles actual data, any interpretation or conclusions drawn here cannot be assumed to represent real conditions in the region. This project primarily demonstrates analytical methods, data processing workflows, and skill development in fisheries and environmental data science.

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

> 📁 For more on the times-series analysis and visualizations using the full dataset, see the **Temporal CPUE Analysis Module** in the [SquidStock](https://github.com/Euchie23/SquidStock).


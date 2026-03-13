# 🗺️ Course Correction — CPUE Standardization & Prediction (2000–2020)


## 🧭 Problem Framing & Data Context
Exploratory temporal analysis (see [*The Navigation Course*](https://github.com/Euchie23/SquidStock/blob/main/notbooks/Temporal_Catch_Analysis/)) identified strong seasonality and long-term CPUE decline, but raw CPUE remained confounded by uneven fishing effort, zero catches, and skewed distributions. To ensure comparability across years and produce indices suitable for management use, CPUE required **formal statistical standardization** capable of handling nonlinear environmental effects and zero-inflated catch processes.

---

## 📘 Executive Summary
Raw CPUE can obscure true population signals due to variation in fishing effort and environmental conditions. This module standardizes squid CPUE for *Illex argentinus* (2000–2020, January–June) using distribution-aware statistical models, producing **bias-corrected indices suitable for fisheries management**.

The standardized CPUE confirms **persistent seasonal peaks (March–May)** and reveals **recurring multi-year variability**, consistent across modeling approaches. Among the tested frameworks, Tweedie-based models provided the strongest predictive performance, while GAM-based models offered interpretable environmental relationships. Together, these outputs deliver **decision-ready CPUE indicators** that separate ecological signal from sampling noise.

---

## 🌍 Value & Applications

This module converts noisy catch records into **reliable indicators of stock performance**, supporting evidence-based decision-making in squid fisheries.

**Supports:**
- Fisheries quota setting and stock status reporting  
- Monitoring productivity under climate and habitat change  
- Separating environmental effects from fishing effort  
- Integration of standardized CPUE into assessment workflows  

---

## 🗃️ Data & Modeling Overview
The analysis uses *Illex argentinus* catch data (2000–2020, January–June) with environmental covariates including:
- Sea Surface Temperature (SST)  
- Sea Surface Height (SSH)  
- Chlorophyll-a (Chl-a)  
- Fishing depth  

Missing environmental values were interpolated to preserve temporal continuity.

CPUE was modeled using **distribution-aware frameworks** designed to accommodate skewness, overdispersion, and nonlinear responses:
- Log-transformed LinearGAMs  
- GammaGAM  
- Tweedie Regressor  

Model selection employed **5-fold cross-validation**, followed by evaluation on an independent hold-out test set.

---

## 📊 Key Results & Interpretation

### Standardization Outcomes

**Observed vs Standardized CPUE:**  
![Observed vs Standardized CPUE](https://github.com/Euchie23/SquidStock/blob/main/outputs/CPUE_Standardization_%26_Prediction/observed_vs_standardized.png)  
  
**Yearly Summary (Jan–Jun):**  
![Yearly Summary](https://github.com/Euchie23/SquidStock/blob/main/outputs/CPUE_Standardization_%26_Prediction/yearly_seasonal_feature_summary.png)  

---

## 🧠 Interpretation & Ecological Implications
Standardized CPUE preserves consistent **seasonal peaks from March to May**, supporting a biological rather than effort-driven signal. Multi-year variability (~8-year scale) emerges across standardized indices, suggesting influence from broader environmental or ecological drivers. Declining standardized CPUE toward the end of the series may reflect reduced productivity or shifts in habitat use rather than sampling artifacts.

---

## 🎯 Applied Use Case — CPUE Standardization for Management
**Objective:** Produce standardized CPUE indices suitable for operational fisheries management.

**Enables:**
- Stock assessment inputs and harvest control rules  
- Consistent inter-annual comparison of squid abundance  
- Detection of environmentally driven shifts in catchability  

An interactive application allows users to explore standardized CPUE trends and environmental context: 
![Dashboard Screenshot](https://drive.google.com/uc?export=view&id=1uR5WzGxvV3coqzcsEk4sD3PcfadjU31T)<br>
[**Launch the App**](https://squidstock-course-correction.streamlit.app)

---

## 📈 Model Evaluation & Selection
Cross-validation results aligned with hold-out test performance, indicating stable generalization across years. The Tweedie Regressor achieved the highest predictive accuracy, while GammaGAM provided stable and interpretable fits of environmental effects.

| Model | RMSE | MAE |
|------|------|-----|
| GAM (log(CPUE + c)) | 863.62 | 472.40 |
| GAM (log(CPUE + 1)) | 880.54 | 504.39 |
| GammaGAM | 810.04 | 458.44 |
| **Tweedie Regressor** | **476.01** | **313.47** |

> **Note:** For additional model validation and detailed diagnostics—including predicted vs actual CPUE and residual plots—please refer to the outputs in this repository:  
> - [Predicted vs Actual CPUE](https://github.com/Euchie23/SquidStock/blob/main/outputs/CPUE_Standardization_%26_Prediction/predicted_vs_actual.png)  
> - [Residual Plots](https://github.com/Euchie23/SquidStock/blob/main/outputs/CPUE_Standardization_%26_Prediction/residuals.png)


---

## 📉 Limitations & Future Work

> While these standardized CPUE indices provide reliable guidance for seasonal stock monitoring and inter-annual comparison, certain data and modeling constraints may affect operational decisions. Managers should consider these caveats when using indices for quota setting, survey planning, or risk assessment.

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


> 🧭 *Overall, future work should aim to integrate spatiotemporal modeling, refine residual structure, and link standardized CPUE variability to external environmental forcing — deepening both predictive accuracy and ecological understanding.*

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

[**Click to see notebook**](https://github.com/Euchie23/SquidStock/blob/main/notebooks/CPUE_Standardization_&_Prediction/CPUE_Standardization_&_Prediction.ipynb)

---

## 🔒 Data Confidentiality Notice

This dataset is a simulated approximation of a real-world squid stock assessment dataset used during my tenure as a part-time research assistant at National Taiwan University. Although it closely resembles actual data, any interpretation or conclusions drawn here cannot be assumed to represent real conditions in the region. This project primarily demonstrates analytical methods, data processing workflows, and skill development in fisheries and environmental data science.

---

## 🤝 Collaboration & Contact

Contributions welcome from fisheries scientists and data analysts.  
Open an issue or submit a pull request to collaborate on future modules.

---
## 📬 Connect

[**Email**](mailto:euchiejnpierre@gmail.com) | [**LinkedIn**](https://linkedin.com/in/euchiejnpierre)  

Thank you for exploring **SquidStock** — advancing sustainable squid fisheries through data transparency and ecological insight.

---

> 🦑 *Project 2 of the [SquidStock](https://github.com/Euchie23/SquidStock) series — advancing data-driven, climate-aware squid fishery modeling.* <br>
> 📌 This project is part 2 of the [**Temporal Catch Analysis Module**](https://github.com/Euchie23/SquidStock/edit/main/notebooks/Temporal_Catch_Analysis/) | 
[Click here for App](https://squidstock-course-correction.streamlit.app).

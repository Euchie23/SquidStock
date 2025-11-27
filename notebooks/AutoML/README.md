# 🦾 ⚙️🦿 The Engine Room: Weekly Squid CPUE Prediction  
### **End-to-End ML Workflow • Feature Engineering • AutoML • Drift & Anomaly Detection**

This repository contains a full machine-learning workflow developed to model **weekly CPUE (Catch-Per-Unit-Effort)** for *Illex argentinus* using environmental and temporal predictors.  
The analysis focuses on **January–June**, the most stable seasonal window for this species.

The goal is not to produce perfect forecasts — CPUE is inherently noisy and influenced by unobserved ecological processes — but to demonstrate a **transparent, scientific, and production-ready ML pipeline**.

---

# 📘 Executive Summary

### **What this project does**
- Builds a **complete ML workflow**: data wrangling, feature engineering, feature selection, classification, class-conditioned regression, model diagnostics, drift detection, and anomaly identification.
- Uses **AutoML (PyCaret)** to compare tree-based methods for both classification and regression.
- Applies **Boruta + manual feature refinement** to ensure ecological interpretability.
- Evaluates performance honestly, identifies weaknesses, and explains why CPUE remains difficult to predict.

### **Main outcome**
- **Classification models performed moderately**, correctly identifying general trends but struggling with Medium CPUE — consistent with ecological expectations.
- **Regression models performed poorly**, with negative R² scores across all CPUE levels.  
  This is *normal* for short-lived cephalopods: CPUE ≠ biomass, and environmental variability is high.
- **Feature drift and anomalies** were detected, reinforcing that CPUE data are unstable and sensitive to fishing behavior.

### **Why this matters**
This project demonstrates real-world ML challenges in fisheries science:  
noisy data, high environmental variability, and the gap between catch rates and true abundance.

The value lies in the **workflow**, **transparency**, and **scientific reasoning**, not in accuracy alone.

---

# 🔒 Data Confidentiality Notice
This project uses a **simulated and anonymized dataset** modeled after patterns observed during my work as a part-time research assistant at **National Taiwan University**.  
It is intended **solely for methodological demonstration and portfolio development**.  
No confidential or proprietary assessment data are used.

---

# 🧩 Project Overview  
**“Learning CPUE with Machine Learning — What Works, What Doesn't.”**

### Core objectives:
- Build temporal + environmental features  
- Learn CPUE *levels* (Low / Medium / High)  
- Model CPUE *within each class* using regression  
- Apply feature selection (Boruta + manual refinement)  
- Detect drift & anomalies  
- Provide interpretable fisheries-relevant insights

---

# 🛠️ Tools & Techniques  
**Core libraries:**  
`pandas`, `numpy`, `scikit-learn`, `PyCaret`, `seaborn`, `matplotlib`

**ML methods implemented:**
- Boruta feature selection  
- Manual feature refinement  
- PyCaret AutoML (classification & regression)  
- Tree-based model comparison  
- Hyperparameter tuning  
- Feature importance extraction  
- Confusion matrices  
- Residual diagnostics  
- Feature drift detection  
- Anomaly detection  

---

# 📊 Data & Features

### **Feature groups used**
- **Temporal:** Year, WeekOfYear, sin/cos seasonality  
- **Environmental:** SST, Chl-a, Depth, lagged depth  
- **Interactions:** Depth × Temperature, Depth × Chl-a  

### **Final feature subsets**
- **Global features** for Low & High CPUE  
- **Medium-specific feature subset**, due to known instability  
- Features regularly shifted over time → **feature drift confirmed**

---

# 🔍 Classification Results (Low / Medium / High)

### 🔧 **Best model: Random Forest Classifier**
- Accuracy: ~0.48  
- F1-score: ~0.46  
- Medium CPUE most difficult (expected due to ecological noise)

### 🧭 **Confusion matrix key insight**
Diagonal hits:  
- Low = **10 correct**  
- Medium = **11 correct**  
- High = **9 correct**

Medium CPUE had the **highest misclassification**, confirming it is the least predictable regime.

### 🐟 Real-World Interpretation
- **Low CPUE** → driven by seasonal timing & depth  
- **High CPUE** → driven by interannual cycles + seasonality  
- **Medium CPUE** → highly unstable, weakly related to environmental predictors

---

# 📈 Regression Results (Class-Conditioned Models)

Regression was applied separately for **Low**, **Medium**, and **High** CPUE.

⚠️ **Key finding: all regression models achieved negative R² values.**  
This means environmental predictors could not explain week-to-week CPUE variation.

This is *normal* for squid fisheries:

- CPUE reflects **aggregation**, not population size  
- Fisher behavior strongly influences catch rates  
- Oceanographic conditions change faster than sampling frequency  

---

## Key Findings by CPUE Level

### **Low CPUE**
- **Best Model:** LightGBM  
- **Performance:** MAE ≈ 1.33, RMSE ≈ 1.93, R² ≈ -0.27  
- **Key Features:** Depth lags, latitude, Temp × Depth interactions  
- **Interpretation:** Weak predictive power; depth drivers help but noise dominates.

---

### **Medium CPUE**
- **Best Model:** LightGBM  
- **Performance:** MAE ≈ 0.45, RMSE ≈ 0.50, R² ≈ -0.59  
- **Key Features:** Depth × Chl-a, latitude, depth lags  
- **Interpretation:** Medium CPUE remains the hardest regime; environmental drivers are insufficient.

---

### **High CPUE**
- **Best Model:** Extra Trees Regressor  
- **Performance:** MAE ≈ 0.39, RMSE ≈ 0.45, R² ≈ -1.15  
- **Key Features:** Year, latitude, sin_week  
- **Interpretation:** Strong seasonality and interannual variability; extreme peaks poorly predicted.

---

# 🚨 Drift & Anomaly Detection

As part of the workflow, we investigated **feature drift** and **data anomalies**:

### Feature Drift (KS Test)
![Feature Drift Plot](https://github.com/Euchie23/SquidStock/blob/main/outputs/Auto_ML/feature_drift_plot.png)

- Most physical/environmental variables (temperature, SSH, chlorophyll, etc.) showed **significant drift** (p < 0.05), meaning they changed between 2000–2015 and 2016–2020.
- Effort- and season-related variables (weekly_effort, WeekOfYear, cos_week, sin_week, Avg_weekly_Lon) did **not drift**, indicating stable fishing timing and fleet distribution across years.

### Anomaly Detection (Isolation Forest)
![Anomaly Detection Counts](https://github.com/Euchie23/SquidStock/blob/main/outputs/Auto_ML/anomaly_detection_counts.png)

- More anomalies were detected in the test period (2016–2020) than in the training period (2000–2015).
- This suggests that recent environmental conditions differ substantially from historical patterns, flagging unusual observations.


---

# 🌎 Real-World Interpretation

### **What this project teaches**
- CPUE is **not a reliable proxy for biomass**  
- Environmental predictors only explain part of the variance  
- Machine learning struggles with unstable ecological processes  
- Classification can approximate general patterns  
- Regression should be paired with ecological models (e.g., EDSPM)

### **Practical fisheries implications**
- Medium CPUE levels are typically noise-dominated  
- Environmental indicators (SST, Chl-a, depth) help characterize Low/High regimes  
- Adaptive management requires **seasonal context**, not raw CPUE predictions

---

# 📉 Limitations & Future Work

### Current limitations
- Small, noisy dataset  
- Monthly satellite resolution (coarse)  
- CPUE influenced by unobserved fisher behavior  
- Medium CPUE has inherent ecological instability  
- Regression R² < 0 across all regimes  
- Feature drift reduces model stability over time  

### Future directions
- Incorporate **effort** and **gear-related** features  
- Use **spatiotemporal models** (GAMs, INLA, VAE-LSTMs)  
- Integrate environmental forecasts (e.g., Niño indices)  
- Expand beyond January–June  
- Combine ML with mechanistic models (e.g., EDSPM)

---

## 🧭 Summary Statement

> This project demonstrates a **rigorous, honest, and transparent application of AutoML** to an ecologically complex problem.  
>
> It reflects the real-world difficulty of predicting CPUE for **short-lived cephalopods**, *Illex argentinus*, and highlights the importance of pairing machine learning with ecological understanding.  
>
> Despite limited predictive performance, the project showcases:  
> - A full scientific ML pipeline  
> - Strong data engineering  
> - Critical interpretation  
> - Real-world fisheries reasoning  
> - Deployment-ready workflow

---
# 📸 Visual Outputs 

### **Classification**
![Temperature-Dependent Growth (EDSPM)](https://github.com/Euchie23/SquidStock/blob/main/outputs/Biomass_Forecasting/temperature_dependent_growth_rate.png) <br><br>

### **Regression**  
- **Panel 1 – Simulated Biomass Under Two Scenarios**
- **Panel 2 – % Change in Biomass Due to Warming**
- **Panel 3 – Environmental Effect Index E(t)**
![biomass_simulation](https://github.com/Euchie23/SquidStock/blob/main/outputs/Biomass_Forecasting/biomass_scenarios_comparison.png)<br><br>

 ### **Drift & Anomalies**  
![cpue_vs_biomass](https://github.com/Euchie23/SquidStock/blob/main/outputs/Biomass_Forecasting/cpue_vs_biomass_comparison.png)

---

## 🔒 Data Confidentiality Notice  

This project uses a simulated and anonymized dataset modeled after patterns observed during my work as a part-time research assistant at National Taiwan University. It is designed exclusively for methodological demonstration and skill development in machine learning, fisheries analysis, and environmental data science. The dataset does not represent official assessments, and no confidential or proprietary information is included.


---

## 🤝 Collaboration & Contact

Contributions and extensions are welcome — especially from researchers working on **cephalopod ecology, stock assessment modeling, or environmental forecasting**.  

📬 [**Email**](mailto:euchiejnpierre@gmail.com) | [**LinkedIn**](https://linkedin.com/in/euchiejnpierre)  
🧠 Explore more modules at [**SquidStock Repository**](https://github.com/Euchie23/SquidStock)

---

> 🦑 *Project 4 of the SquidStock series — Predictive Modelling*

# 🦾 ⚙️🦿 The Engine Room: Predictive Catch Modelling  
### **End-to-End ML Workflow • Feature Engineering • AutoML • Drift & Anomaly Detection**

## 🌍 Real-World Value

The Engine Room showcases a **full, production-ready ML workflow** applied to one of the hardest real-world problems in fisheries science: predicting weekly CPUE for a fast-moving, environmentally sensitive species.  
Instead of chasing unrealistic accuracy, it demonstrates **transparent, rigorous machine-learning practice** under real ecological constraints.

### Who This Helps
- **Fisheries agencies:** evaluate when CPUE trends are meaningful vs. noise  
- **Environmental data teams:** understand drift, anomalies, and shifting ecological regimes  
- **ML engineers / data scientists:** see how to build robust pipelines on unstable, non-stationary datasets  
- **Research groups:** explore how ML complements (not replaces) ecological models  

### Why It Matters
Squid CPUE is highly variable, often decoupled from abundance, and driven by rapid ocean changes.  
This project adds value not by accuracy alone, but by demonstrating:

- Feature engineering tailored for ecological time series  
- Class-conditioned modeling for asymmetric CPUE behavior  
- Drift + anomaly detection to flag shifting environmental regimes  
- Honest model diagnostics that explain *why* predictions are difficult  
- A workflow that would be deployable in real fisheries or environmental monitoring systems  

In a field where many models overpromise, **The Engine Room shows what responsible, scientifically grounded ML looks like** — and how to interpret results in an ecological context.  
It highlights ML strengths, limitations, and how data instability shapes real management decisions.

---

This project contains a full machine-learning workflow developed to model **weekly CPUE (Catch-Per-Unit-Effort)** for *Illex argentinus* using environmental and temporal predictors.  
The analysis focuses on **January–June**, the most stable seasonal window for this species.

The goal is not to produce perfect forecasts — CPUE is inherently noisy and influenced by unobserved ecological processes — but to demonstrate a **transparent, scientific, and production-ready ML pipeline**.

---

# 📘 Executive Summary

### **What this project does**
- Builds a **complete ML workflow**: data wrangling, feature engineering, feature selection, classification, class-conditioned regression, model diagnostics, drift detection, and anomaly identification.
- Uses **AutoML (PyCaret)** to compare tree-based methods for both classification and regression.
  -   Only **tree-based models** were used for both classification and regression because they:
      - Handle **nonlinear relationships** and **feature interactions** naturally, which are common in CPUE data.
      - Are robust to **outliers** and **missing values**, frequent in ecological datasets.
      - Offer **feature importance measures**, helping link model outputs to ecological drivers.
      - Perform well even when the target variable is **log-transformed**, as in our regression models (CPUE_log1p), to stabilize variance and reduce skew.
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
- Confusion matrix  
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

> *Go to Visual Outputs section below to view the confusion mtrix*

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

> *Go to Visual Outputs section below to view the residual plots*

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
[Feature Drift Plot](https://github.com/Euchie23/SquidStock/blob/main/outputs/AutoML/feature_drift_plot.png)

- Most physical/environmental variables (Average Weekly Water Temperature, Sea Surface (SSH), Chlorophyll_A, Average Weekly Depth and Average Weekly Latitude and Longitude etc..) showed **significant drift** (p < 0.05), meaning they changed between 2000–2015 and 2016–2020.
- Effort- and season-related variables (weekly_effort, cos_week, sin_week) did **not drift**, indicating stable fishing timing across years.

### Anomaly Detection (Isolation Forest)
[Anomaly Detection Counts](https://github.com/Euchie23/SquidStock/blob/main/outputs/AutoML/anomaly_detection_counts.png)

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
![Confusion Matrix](https://github.com/Euchie23/SquidStock/blob/main/outputs/AutoML/classification_confusion_matrix.png) <br><br>

### **Regression**  
![Regression Residuals Low CPUE](https://github.com/Euchie23/SquidStock/blob/main/outputs/AutoML/regression_residuals_Low.png)
![Regression Residuals Medium CPUE](https://github.com/Euchie23/SquidStock/blob/main/outputs/AutoML/regression_residuals_Medium.png)
![Regression Residuals High CPUE](https://github.com/Euchie23/SquidStock/blob/main/outputs/AutoML/regression_residuals_High.png)<br><br>

 ### **Feature Drift & Anomaly Detection**  
![Drift Summary](https://github.com/Euchie23/SquidStock/blob/main/outputs/AutoML/feature_drift_plot.png)
![Anomaly Detection](https://github.com/Euchie23/SquidStock/blob/main/outputs/AutoML/anomaly_detection_counts.png)<br><br>

---

## 🤝 Collaboration & Contact

Contributions and extensions are welcome — especially from researchers working on **cephalopod ecology, stock assessment modeling, or environmental forecasting**.  

📬 [**Email**](mailto:euchiejnpierre@gmail.com) | [**LinkedIn**](https://linkedin.com/in/euchiejnpierre)  
🧠 Explore more modules at [**SquidStock Repository**](https://github.com/Euchie23/SquidStock)

---

> 🦑 *Project 4 of the SquidStock series — Predictive Modelling*

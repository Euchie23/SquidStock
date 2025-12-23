# 🦾 ⚙️🦿 The Engine Room: Weekly Squid CPUE Prediction
### **End-to-End ML Workflow • Feature Engineering • AutoML • Drift & Anomaly Detection**

## 📘 Executive Summary  
This module implements a full machine-learning workflow to model weekly CPUE for *Illex argentinus*, focusing on January–June (the most stable seasonal window).  

**Key Findings:**

- Weekly CPUE is highly unstable and weakly predictable from environmental variables.  
- Classification models moderately identify general CPUE regimes (Low / Medium / High), but Medium CPUE is least predictable.  
- Regression models (class-conditioned) achieve negative R² values — expected for short-lived, mobile cephalopods.  
- Feature drift and anomalies were detected, emphasizing that CPUE is sensitive to environmental change and fishing behavior.  

**Management Insight:** This workflow allows managers to distinguish meaningful CPUE signals from noise, avoiding premature reactions to short-term fluctuations.

---

## 📈 Real-World Value  
This module demonstrates a production-ready ML workflow for ecological time series with unstable targets.  

**Who This Helps:**

- Fisheries agencies: detect meaningful CPUE trends vs noise  
- Environmental data teams: monitor drift, anomalies, and shifting regimes  
- ML engineers / data scientists: build robust pipelines on noisy, non-stationary datasets  
- Research groups: explore ML complementing ecological models  

**Why It Matters:** CPUE is decoupled from abundance; environmental predictors explain only part of the variance. A transparent, interpretable ML pipeline supports informed, adaptive management.  

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

![Confusion Matrix](https://github.com/Euchie23/SquidStock/blob/main/outputs/AutoML/classification_confusion_matrix.png) <br>
Medium CPUE had the **highest misclassification**, confirming it is the least predictable regime.


### 🐟 Real-World Interpretation
- **Low CPUE** → driven by seasonal timing & depth  
- **High CPUE** → driven by interannual cycles + seasonality  
- **Medium CPUE** → highly unstable, weakly related to environmental predictors

---

# 📈 Regression Results (Class-Conditioned Models)

Regression was applied separately for **Low**, **Medium**, and **High** CPUE.
> *See residual plots below for your reference* 
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
![Regression Residuals Low CPUE](https://github.com/Euchie23/SquidStock/blob/main/outputs/AutoML/regression_residuals_Low.png)
---

### **Medium CPUE**
- **Best Model:** LightGBM  
- **Performance:** MAE ≈ 0.45, RMSE ≈ 0.50, R² ≈ -0.59  
- **Key Features:** Depth × Chl-a, latitude, depth lags  
- **Interpretation:** Medium CPUE remains the hardest regime; environmental drivers are insufficient.
![Regression Residuals Medium CPUE](https://github.com/Euchie23/SquidStock/blob/main/outputs/AutoML/regression_residuals_Medium.png)
---

### **High CPUE**
- **Best Model:** Extra Trees Regressor  
- **Performance:** MAE ≈ 0.39, RMSE ≈ 0.45, R² ≈ -1.15  
- **Key Features:** Year, latitude, sin_week  
- **Interpretation:** Strong seasonality and interannual variability; extreme peaks poorly predicted.
![Regression Residuals High CPUE](https://github.com/Euchie23/SquidStock/blob/main/outputs/AutoML/regression_residuals_High.png)
---

# 🚨 Drift & Anomaly Detection

As part of the workflow, we investigated **feature drift** and **data anomalies**:

### Feature Drift (KS Test)
![Feature Drift Plot](https://github.com/Euchie23/SquidStock/blob/main/outputs/AutoML/feature_drift_plot.png)

- Most physical/environmental variables (Average Weekly Water Temperature, Sea Surface (SSH), Chlorophyll_A, Average Weekly Depth and Average Weekly Latitude and Longitude etc..) showed **significant drift** (p < 0.05), meaning they changed between 2000–2015 and 2016–2020.
- Effort- and season-related variables (weekly_effort, cos_week, sin_week) did **not drift**, indicating stable fishing timing across years.

### Anomaly Detection (Isolation Forest)
![Anomaly Detection Counts](https://github.com/Euchie23/SquidStock/blob/main/outputs/AutoML/anomaly_detection_counts.png)

- More anomalies were detected in the test period (2016–2020) than in the training period (2000–2015).
- This suggests that recent environmental conditions differ substantially from historical patterns, flagging unusual observations.

---

## 🧩 Module Overview  
**Core Objectives:**

- Build temporal and environmental features  
- Classify weekly CPUE into Low / Medium / High  
- Apply class-conditioned regression models  
- Detect feature drift and anomalies  
- Provide interpretable insights for fisheries management  

Outcome: Guides adaptive management decisions by highlighting where CPUE trends are ecologically meaningful vs noise-dominated.  

---

## 🧮 Model Specification  
- **Classification:** Random Forest Classifier (Low / Medium / High CPUE)  
- **Regression (class-conditioned):** LightGBM / Extra Trees per CPUE class  
- **Feature selection:** Boruta + manual refinement  
- **Drift detection:** KS Test (2000–2015 vs 2016–2020)  
- **Anomaly detection:** Isolation Forest  
- **Evaluation:** Confusion matrix, residuals, R², MAE, RMSE

---

🎯 Applied Use Case  
Scenario: Detecting meaningful CPUE trends in fisheries management  

- Sharp weekly CPUE drop? Use drift detection + anomaly flags to distinguish:
  - Environmental regime shift (drift)  
  - Unusual observation (anomaly)  
  - Normal variability (prediction unreliable)  
- **Management implication:** Avoid overreacting to short-term CPUE fluctuations; focus on regime-level changes and seasonal context.  
- **Interactive App:** Explore weekly CPUE predictions and anomaly alerts in an intuitive interface: [Launch the App](https://squidstock-the-engine-room.streamlit.app)  

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

## 🛠️ How to Run This Notebook

1. Clone this repository. 
      -  git clone https://github.com/Euchie23/SquidStock.git
2. Ensure you have Python 3 installed. 

3. Install dependencies via pip:
      -  e.g., pip install pandas numpy matplotlib seaborn statsmodels pygam, pycaret jupyter
        
4. Launch Jupyter Notebook and open /notebooks/AutoML.ipynb
   
5. Run cells sequentially to reproduce the analysis.
   
[See notebook for reference](https://github.com/Euchie23/SquidStock/blob/main/notebooks/Biomass_Forecasting/AutoML.ipynb).

---

# 🔒 Data Confidentiality Notice
This project uses a **simulated and anonymized dataset** modeled after patterns observed during my work as a part-time research assistant at **National Taiwan University**.  
It is intended **solely for methodological demonstration and portfolio development**.  
No confidential or proprietary assessment data are used.

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

This project demonstrates a **rigorous, honest, and transparent application of AutoML** to an ecologically complex problem.  

It reflects the real-world difficulty of predicting CPUE for **short-lived cephalopods**, *Illex argentinus*, and highlights the importance of pairing machine learning with ecological understanding.  

 Despite limited predictive performance, the project showcases:  
 - A full scientific ML pipeline  
 - Strong data engineering  
 - Critical interpretation  
 - Real-world fisheries reasoning  
 - Deployment-ready workflow

---

## 🤝 Collaboration & Contact

Contributions and extensions are welcome — especially from researchers, data scientists, fisheries experts or consultants working on **cephalopod/marine ecology, stock assessment modeling, or environmental forecasting**.  

📬 [**Email**](mailto:euchiejnpierre@gmail.com) | [**LinkedIn**](https://linkedin.com/in/euchiejnpierre)  

---

> 🦑 *Project 4 of the [SquidStock](https://github.com/Euchie23/SquidStock) series — advancing data-driven, climate-aware squid fishery modeling.* <br>
> 📌 This project is the continuation of [**Temporal_Catch_Analysis Module**](https://github.com/Euchie23/SquidStock/edit/main/notebooks/Temporal_Catch_Analysis/README.md), [**CPUE_Standardization_&_Prediction (2000-2020)**](https://github.com/Euchie23/SquidStock/tree/main/notebooks/CPUE_Standardization_%26_Prediction/README.md) and
> [**Predictive Catch Modelling**](https://github.com/Euchie23/SquidStock/tree/main/notebooks/AutoML/README.md) 

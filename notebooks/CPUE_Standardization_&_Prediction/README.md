# 📘 Module 2 — CPUE Standardization & Modeling (2010–2020)

This notebook advances the *SquidStock* analytical series by standardizing and modeling *Illex argentinus* catch data (2010–2020).  
Building on the exploratory work in **Module 1**, it applies **Generalized Additive Models (GAMs)** and **Tweedie GLMs** to remove effort bias and reveal underlying ecological structure in **Catch Per Unit Effort (CPUE)**.

---

## 🎯 Executive Summary

This module develops a **robust, reproducible workflow** for CPUE standardization using a 10-year subset (**January – June each year**).  
These months were selected for their **consistent data coverage** across all years, ensuring comparability and avoiding partial-year bias.

To address missing satellite-derived environmental data (Chl-a, SSH, Depth), **linear interpolation** was applied — filling temporal gaps while preserving natural monthly trends.  
Linear interpolation estimates missing values between two known points using a straight-line assumption, making it transparent and appropriate for smooth, seasonal environmental data.

### 🔍 Key Insights
- **GammaGAM** and **TweedieGLM** delivered superior fit and stability relative to log-transformed GAMs.  
- **5-fold cross-validation** confirmed **GammaGAM** slightly outperformed others, while **TweedieGLM** remained most robust under overdispersion.  
- Residual diagnostics showed well-behaved errors and minimal bias.  
- Seasonal peaks (March – May) persisted after standardization, confirming **biological (e.g migration) rather than effort-driven** variability.

Together, these findings validate flexible, distribution-aware models as strong tools for squid fishery standardization.

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
2. **Exploratory Analysis:** Examine CPUE distributions, environmental variability, and correlations.  
3. **Yearly Summary:** Compute mean ± SD for key variables (Jan–Jun subset).  
4. **Modeling:** Fit LinearGAM, GammaGAM, and Tweedie GLM frameworks.  
5. **Evaluation:** Compare performance metrics (RMSE / MAE).  
6. **Diagnostics:** Inspect residuals and fitted vs observed trends.  
7. **Outputs:** Generate standardized CPUE time-series and visual summaries.  

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
| **Monthly CPUE mean** | ↓ Declining | Highly variable; overall decrease from early 2000s (≈14 605 kg) to 2019 (≈ 4 053 kg). Suggests declining productivity or catchability. |
| **Water Temperature mean** | ↑ Increasing | Gradual warming (≈ 10.99 → 11.41 °C). May drive squid to deeper / southern waters, lowering CPUE. |
| **SSH mean** | ↑ Increasing | Rising SSH (0.01 → 0.08 m) could signal reduced upwelling and nutrient supply, impacting productivity. |
| **Chlorophyll-a mean** | → Stable / slightly decreasing | Mixed pattern; productivity fluctuations don’t always boost CPUE, indicating trophic mismatch. |
| **Depth mean** | ↑ Increasing | Fishing depth rose (≈ 92 → 152 m), implying migration to cooler zones. May reflect adaptive fishing or habitat shifts. |

📄 [**Yearly Summary (2000 – 2020, Jan–Jun Subset)**](https://github.com/Euchie23/SquidStock/blob/main/outputs/CPUE_Standardization_%26_Prediction/yearly_seasonal_feature_summary.png)  
→ *Trends derived from descriptive summary (mean, SD, min, max) with directional arrows for clarity.*
→ *Arrow Color Key: Red ↑↓ = Negative/Unfavorable Trend | Green ↑↓ = Positive/Favorable Trend | Black → = Stable/No Change*
---

## 🧠 Modeling Framework

| Model | Transformation | Distribution | Strength |
|:------|:----------------|:--------------|:----------|
| **LinearGAM (log(CPUE + c))** | Variance stabilization | Normal | Interpretable baseline |
| **LinearGAM (log(CPUE + 1))** | Benchmark log-scale | Normal | Consistent comparison |
| **Gamma GAM** | Raw CPUE | Gamma | Best for positive, right-skewed data |
| **Tweedie GLM** | Raw CPUE | Tweedie | Robust to zero-inflation & overdispersion |

All models were evaluated via **5-fold cross-validation** using RMSE and MAE.

---

## 🧾 Model Evaluation Results

| Model | RMSE | MAE |
|:------|------:|------:|
| GAM (log(CPUE + c)) | 16 673 | 10 089 |
| GAM (log(CPUE + 1)) | 15 986 | 9 638 |
| **Gamma GAM** | 15 688 | 9 305 |
| **Tweedie GLM** | 13 282 | 8 177 |

**Cross-validation means (RMSE):**  
LinearGAM (+c) = 12 921 | LinearGAM (+1) = 15 414 | Gamma GAM = 11 211 | Tweedie GLM = 12 534  

📊 [**Model Performance (PNG)**](https://github.com/Euchie23/SquidStock/blob/main/outputs/CPUE_Standardization_%26_Prediction/model_performance.png)  
📄 [**Model Performance (PDF)**](https://github.com/Euchie23/SquidStock/blob/main/outputs/CPUE_Standardization_%26_Prediction/model_performance.pdf)

> 🧠 *Gamma GAM and Tweedie GLM consistently yielded lower errors, supporting their suitability for skewed ecological data.*

---

## 📈 Core Visualizations & Diagnostics

| Visualization | Output | Purpose |
|---------------|-----------|----------|
| **Observed vs Standardized CPUE** | [PNG File](https://github.com/Euchie23/SquidStock/blob/main/outputs/CPUE_Standardization_%26_Prediction/observed_vs_standardized.png) / [HTML File](https://github.com/Euchie23/SquidStock/blob/main/outputs/CPUE_Standardization_%26_Prediction/observed_vs_standardized.png) | Compare raw and standardized indices |
| **Predicted vs Actual CPUE** | [PNG File](https://github.com/Euchie23/SquidStock/blob/main/outputs/CPUE_Standardization_%26_Prediction/predicted_vs_actual.png) | Assess predictive accuracy |
| **Residual Plots** |[PNG File](https://github.com/Euchie23/SquidStock/blob/main/outputs/CPUE_Standardization_%26_Prediction/residuals.png) | Check error distribution |
| **Model Performance Table** | [PNG File](https://github.com/Euchie23/SquidStock/blob/main/outputs/CPUE_Standardization_%26_Prediction/model_performance.png) | Summarize RMSE / MAE |
| **Yearly Summary (Jan–Jun)** | [PNG File](https://github.com/Euchie23/SquidStock/blob/main/outputs/CPUE_Standardization_%26_Prediction/yearly_summary_JanJun.png) | Context for environmental trends |

🕹️ Interactive versions (`.html`) are available for dowload by right clicking.

---

## 🧭 Interpretation of Model Results

- **Gamma GAM**: Most stable residuals; fits right-skewed CPUE effectively.  
- **Tweedie GLM**: Resilient to overdispersion; strongest on variable data.  
- **Log GAMs**: Underpredict high CPUE due to transformation compression.  
- **Standardized Indices**: Seasonal peaks persist → biologically driven variation.  

✅ These diagnostics confirm **robust, ecologically meaningful** standardization.

---

## 🌍 Real-World Applications

- Enhanced **stock assessment** and quota setting  
- Detection of **environmental thresholds** in squid abundance  
- Support for **ecosystem-based fisheries management**  
- Demonstration of transparent, reproducible modeling workflow  

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

## 📉 Limitations & Future Work

- Data restricted to **Jan–Jun** → while this ensures temporal consistency across years, it excludes potential **late-season dynamics (Jul–Dec)**, which may slightly limit full-year representativeness.  
- Linear interpolation assumes steady change; future versions may test splines or spatiotemporal models.  
- Expanding predictor set (wind, salinity, front indices) could enhance ecological resolution.  

---

## 🤝 Collaboration & Contact

Contributions welcome from fisheries scientists and data analysts.  
Open an issue or submit a pull request to collaborate on future modules.

📬 **Email:** your.email@example.com  
💼 **LinkedIn:** [your-profile-link]  

---

## 🔒 Data Confidentiality Notice

This dataset is a synthetic approximation of research data used at National Taiwan University.  
While statistical patterns reflect realistic conditions, data are non-sensitive and intended solely for educational and methodological demonstration.

---

## 📸 Static Previews

- ![PNG File](https://github.com/Euchie23/SquidStock/blob/main/outputs/CPUE_Standardization_%26_Prediction/observed_vs_standardized.png)  
- ![PNG File](https://github.com/Euchie23/SquidStock/blob/main/outputs/CPUE_Standardization_%26_Prediction/predicted_vs_actual.png)  
- ![PNG File](https://github.com/Euchie23/SquidStock/blob/main/outputs/CPUE_Standardization_%26_Prediction/residuals.png)  
- [PNG File](https://github.com/Euchie23/SquidStock/blob/main/outputs/CPUE_Standardization_%26_Prediction/yearly_summary_JanJun.png)  


---

> 📁 For more on the times-series analysis and visualizations using the full dataset, see the **Temporal CPUE Analysis Module** in the [SquidStock GitHub Repo](https://github.com/Euchie23/SquidStack).


# 🐙📈 SquidStock — Charting Squid Catch Trends & Sustainable Fisheries

## 🌍 Real-World Value

SquidStock transforms 21 years of catch and environmental data into **actionable insights for sustainable fisheries management**.  
It links fishing trends, ocean conditions, and predictive models to help organizations understand how squid stocks respond to climate variability, fishing pressure, and environmental change.

### Who This Helps
- **Fisheries agencies:** monitor long-term catch trends & regime-level CPUE patterns  
- **Marine managers:** integrate CPUE standardization, anomaly detection, and predictive insights into planning  
- **NGOs & policy groups:** assess sustainability trajectories using transparent analytics  
- **Data scientists & researchers:** explore reproducible workflows for ecological time-series forecasting  

### Why It Matters
Squid fisheries are economically important but under-modeled.  
SquidStock fills this gap with accessible, reproducible tools that support **evidence-based harvest decisions**, climate-aware stock assessments, and adaptive ecosystem management.

---

**SquidStock** is part of the curated public side of the `Squid_Fest` project, focusing on 21 years (2000–2020) of *Illex argentinus* catch data.<br><br> 
While **SquidStack** explored pollutant bioindicators in remote locations, **SquidStock** surveyed the ocean shelf and coastal waters — using stock assessments, environmental modeling, and predictive tools to surface hidden patterns across familiar seas.  
> 🛂 This repository hosts curated dashboards and notebooks. The full research pipeline and experimental modules live in the private `Squid_Fest` repo. To request access or collaborate, [email me](mailto:euchiejnpierre@gmail.com).

---

Stock assessments are common in finfish fisheries but rare in squid fisheries, particularly with integrated environmental modeling, predictive dashboards, and workflow automation — that’s where SquidStock brings novelty.

---

## 📂 Repository Structure

- `/notebooks` — Jupyter notebooks including each module’s analysis pipeline.  
- `/outputs` — Generated static plots, tables, and figures.  
- `/data` — Raw and processed datasets (anonymized/simulated for public use).  

---

## 📦 Project Modules & Flow

| Module | Stage name | What It Does | Status | Link | App | Tour |
|---|---|----------------|--------|----------|---------|--------|
| [**Temporal Catch Analysis**](https://github.com/Euchie23/SquidStock/blob/main/notebooks/Temporal_Catch_Analysis/Temporal_Catch_Analysis.ipynb)  | *The Navigation Course* | Time-series of squid catch (CPUE) across years, with environmental summaries and trend indicators | ✅ Complete | [View README](https://github.com/Euchie23/SquidStock/blob/main/notebooks/Temporal_Catch_Analysis) | Animated map in app | - |
| [**CPUE Standardization & Prediction**](https://github.com/Euchie23/SquidStock/blob/main/notebooks/CPUE_Standardization_&_Prediction/CPUE_Standardization_&_Prediction.ipynb) | *Course Correction* | Normalize catch via GAM/GLM; compare prediction performance | ✅ Complete | [View README](https://github.com/Euchie23/SquidStock/blob/main/notebooks/CPUE_Standardization_&_Prediction)  | [🧭 Course Correction](https://squidstock-course-correction.streamlit.app) | - |
| [**Biomass Forecasting + Environment**](https://github.com/Euchie23/SquidStock/blob/main/notebooks/Biomass_Forecasting/Biomass_Forecasting_Environment.ipynb)  | *Ocean Dynamics* | Surplus production modeling including environmental drivers (SST, SSH, Chl‑a) | ✅ Complete | [View README](https://github.com/Euchie23/SquidStock/blob/main/notebooks/Biomass_Forecasting)  | [🌊 Ocean Dynamics](https://squidstock-ocean-dynamics.streamlit.app) | [🎥 Watch Tour](https://youtu.be/UeumWYCHvPI) |
| [**Weekly CPUE Prediction & AutoML**](https://github.com/Euchie23/SquidStock/blob/main/notebooks/AutoML/AutoML.ipynb) | *The Engine Room* | End-to-end ML workflow: weekly CPUE classification, class-conditioned regression, anomaly & drift detection, predictive dashboards | ✅ Complete | [View README](https://github.com/Euchie23/SquidStock/blob/main/notebooks/AutoML) | [⚙️ The Engine Room](https://squidstock-the-engine-room.streamlit.app)  | - |
| **(Future) MLOps / Deployment + Versioning** | *Launch Control* | Model deployment, versioning, monitoring; experimental | 🚀 Future Goal | 🔄 TBD | 🔄 TBD | - |

---

## 🎯 Objectives

- Normalize and standardize catch data through CPUE modeling  
- Examine environmental drivers of squid abundance  
- Forecast biomass and CPUE responses under climate variability  
- Build predictive ML models with AutoML pipelines  
- Support adaptive management and operational decision-making  
- (Future) Deploy, version, and monitor models in production  

---

## 🛠 Tools & Techniques

- **Data & Arrays:** `pandas`, `numpy`, `xarray`, `netCDF4`  
- **Statistical & Predictive Modeling:** `matplotlib`, `pygam`, `scipy`, `statsmodels` (GAM, GLM, Tweedie)  
- **AutoML / ML:** `scikit-learn`, `PyCaret`  
- **Visualization:** `seaborn`  
- **Spatial & Dashboards:** `folium`, `plotly`, `streamlit`  
- **Remote Sensing Processing:** Chlorophyll‑a and SSH extraction from NetCDF layers  
- **Missing Data Handling:** interpolation and neighbor-based imputation for robustness  
- **Development Environment:** Jupyter Notebooks, VSCode  

---

## 📌 Data & Method Highlights

- Base dataset: `catch_kg`, `longitude`, `latitude`, `vessel_id`, `SST`, `depth`, `year`, `month`, `day`  
- Augmented with satellite layers (Chlorophyll‑a, SSH)  
- Missing environmental values imputed to preserve time-series continuity  
- Modeling workflows include:  
  - GAM/GLM-based CPUE normalization and prediction  
  - Environmentally dependent surplus production modeling  
  - AutoML pipelines for weekly/daily CPUE prediction: classification, regression, anomaly detection, feature drift, hyperparameter tuning, feature engineering, tree-based models  
  - Residual diagnostics & cross-validation  
  - Monte Carlo simulations for uncertainty assessment  

---

## 👥 Audience & Use Cases

Useful for:

- Fisheries scientists & marine ecologists  
- Data scientists in environmental or ecological modeling  
- Students in stock assessment, ecological statistics, or ML for ecology  
- NGOs and policymakers seeking operationally relevant predictive insights  

---

## 📬 Get Involved

- 🐛 [Open an issue](https://github.com/Euchie23/SquidStock/issues) for feedback, bugs, or suggestions  
- ✉️ [Email me](mailto:euchiejnpierre@gmail.com) for collaboration or access to `Squid_Fest`  
- 💼 [Connect on LinkedIn](https://www.linkedin.com/in/euchiejnpierre/)  

---

> Thank you for exploring **SquidStock** — a voyage through catch, environment, and predictive insight supporting **sustainable squid fisheries**.

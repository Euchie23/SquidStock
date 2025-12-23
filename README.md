# 🐙📈 SquidStock — Charting Squid Catch Trends & Sustainable Fisheries

## 🌍 Real-World Value

SquidStock transforms 20 years of catch and environmental data into **actionable insights for sustainable fisheries management**.  
It links fishing trends, ocean conditions, and predictive models to help organizations understand how squid stocks respond to climate variability and fishing pressure.

### Who This Helps
- **Fisheries agencies:** monitor long-term catch trends & stock stress indicators  
- **Marine managers:** integrate CPUE normalization and environmental drivers into planning  
- **NGOs & policy groups:** assess sustainability trajectories using transparent analytics  
- **Data scientists:** explore reproducible workflows for ecological time-series forecasting  

### Why It Matters
Squid fisheries are economically important but under-modeled.  
SquidStock fills this gap with accessible, reproducible tools that support **evidence-based harvest decisions**, climate-aware stock assessments, and proactive ecosystem management.

---

**SquidStock** is part of the curated public side of the `Squid_Fest` project, focusing on 20 years (2000–2020) of *Illex argentinus* catch data.<br><br> 
Let’s set the scene:<br> 
**SquidStack** dove deep into pollutant bioindicators — like exploring a remote underwater trench which is rare, rigorous, and deeply exploratory — while **SquidStock** surveyed the ocean shelf and coastal waters (including that same trench), using stock assessments, environmental modeling, and predictive tools to surface hidden patterns across familiar seas.
> 🛂 This repository hosts curated dashboards and analysis. The full research pipeline and experimental modules live in the private `Squid_Fest` repo. To request access or collaborate, [email me](mailto:euchiejnpierre@gmail.com).

---

Though stock assessments are relatively common in finfish fisheries, they are much less frequent in squid fisheries, particularly with rich environmental modeling and predictive dashboards — that’s where this project brings novelty.

---

## 📂 Repository Structure

- `/notebooks` — Jupyter notebooks including The Navigation Course. Each notebook has its own README.md (like this one).  
- `/outputs` — Generated static plot PDFs and summary tables.  
- `/data` — Raw and processed datasets.

---

## 📦 Project Modules & Flow

Here’s how your work is structured, moving from exploration to deployment:

| Module | Stage name | What It Does | Status | Link | App |
|---|---|----------------|--------|----------|---------|
| [**Temporal Catch Analysis**](https://github.com/Euchie23/SquidStock/blob/main/notebooks/Temporal_Catch_Analysis/Temporal_Catch_Analysis.ipynb)  | *The Navigation Course* | Time-series of squid catch (CPUE) across years, with environmental summaries and trend indicators | ✅ Complete | [View README](https://github.com/Euchie23/SquidStock/blob/main/notebooks/Temporal_Catch_Analysis) | See animated map in app below |
| [**CPUE Standardization & Prediction**](https://github.com/Euchie23/SquidStock/blob/main/notebooks/CPUE_Standardization_&_Prediction/CPUE_Standardization_&_Prediction.ipynb) | *Course Correction* | Normalize catch via GAM/GLM, compare prediction performance | ✅ Complete | [View README](https://github.com/Euchie23/SquidStock/blob/main/notebooks/CPUE_Standardization_&_Prediction)  | [ 🧭 Course Correction](https://squidstock-course-correction.streamlit.app) |
| [**Biomass Forecasting + Environment**](https://github.com/Euchie23/SquidStock/blob/main/notebooks/Biomass_Forecasting/Biomass_Forecasting_Environment.ipynb)  | *Ocean Dynamics* | Surplus production modeling including environmental drivers (SST, SSH, Chl‑a) | ✅ Complete | [View README](https://github.com/Euchie23/SquidStock/blob/main/notebooks/Biomass_Forecasting)  | [🌊 Ocean Dynamics](https://squidstock-ocean-dynamics.streamlit.app)  |
| [**AutoML / Predictive Catch Models**](https://github.com/Euchie23/SquidStock/blob/main/notebooks/AutoML/AutoML.ipynb) | *The Engine Room* | Automated modeling pipelines for daily/weekly catch | ✅ Complete | [View README](https://github.com/Euchie23/SquidStock/blob/main/notebooks/AutoML) | [⚙️ The Engine Room](https://squidstock-the-engine-room.streamlit.app)  |
| **(Future) MLOps / Deployment + Versioning** | *Launch Control* | Model deployment, versioning, monitoring; experimental | 🚀 Future Goal | 🔄 TBD | 🔄 TBD |

---

## 🎯 Objectives

- Normalize catch data through CPUE modeling  
- Examine relationships between catch and environmental variables  
- Forecast biomass responses under climate variability  
- Build predictive models using AutoML  
- (Future) Deploy models and manage them in a reproducible workflow

---

## 🛠 Tools & Techniques Used

- **Data & Arrays:** `pandas`, `numpy`, `xarray`, `netCDF4`  
- **Statistical & Predictive Modeling:**  `matplotlib`, `pygam`, `scipy`, `statsmodels` (GAM, GLM, Tweedie)  
- **AutoML / Machine Learning:** `scikit-learn`, `PyCaret`
- **Visualization:** `seaborn`
- **Spatial & Dashboard Tools:** `folium`, `plotly`, `streamlit`  
- **Remote Sensing Processing:** extraction of Chlorophyll‑a and SSH from NetCDF layers  
- **Missing Data Imputation:** median of nearby spatial/temporal neighbors — chosen for stability across gaps and variable neighbor distributions  
- **Development Environment:** Jupyter Notebooks, VSCode  

---

## 📌 Data & Method Highlights

- Base dataset included: `catch_kg`, `longitude`, `latitude`, `vessel_id`, `SST`, `depth`, `year`, `month`, `day`  
- Augmented with satellite layers (Chlorophyll‑a, SSH) pulled from NASA / Copernicus portals  
- Missing environmental values imputed via linear interpolation to mitigate influence of extreme values or sparse coverage
- Modeling workflows:
  - GAMs, GLMs for CPUE normalization and prediction  
  - Environmentally dependent surplus production model for biomass forecasts  
  - AutoML experiments for short-term catch prediction (anomaly detection, hyperparameter tuning, feature drift, feature engineering, tree-based model comparison, model evaluation metrics, etc)
  - Residuals Diagnostics & Cross Validation
  - Nonlinear temperature-dependent modelling
  - Monte Carlo simulations for uncertainty in biomass forecasting 

---

## 👥 Audience & Use Cases

This project is useful for:

- Fisheries scientists & marine ecologists  
- Data scientists working in environmental time series or predictive modeling  
- Students in stock assessment or ecological modeling  
- NGOs / policymakers seeking applied forecasts for sustainable management

---

## 📬 Get Involved

- 🐛 [Open an issue](https://github.com/Euchie23/SquidStock/issues) — for feedback, bugs, or suggestions  
- ✉️ [Email me](mailto:euchiejnpierre@gmail.com) — for collaboration or private access to `Squid_Fest`  
- 💼 [Connect on LinkedIn](https://www.linkedin.com/in/euchiejnpierre/)

---

> Thank you for exploring **SquidStock** — joining a voyage of catch, environment, and predictive insight to support sustainable squid fisheries.  

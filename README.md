# 🐙📈 SquidStock — Charting Squid Catch Trends & Sustainable Fisheries

**SquidStock** is part of the curated public side of the `Squid_Fest` project, focusing on 10 years (2010–2020) of *Illex argentinus* catch data.<br><br> 
Let’s set the scene:<br> 
**SquidStack** dove deep into pollutant bioindicators — like exploring a remote underwater trench which is rare, rigorous, and deeply exploratory — while **SquidStock** surveyed the ocean shelf and coastal waters (including that same trench), using stock assessments, environmental modeling, and predictive tools to surface hidden patterns across familiar seas.
> 🛂 This repository hosts curated dashboards and analysis. The full research pipeline and experimental modules live in the private `Squid_Fest` repo. To request access or collaborate, [email me](mailto:euchiejnpierre@gmail.com).

---

Though stock assessments are relatively common in finfish fisheries, they are much less frequent in squid fisheries, particularly with rich environmental modeling and predictive dashboards — that’s where this project brings novelty.

---

## 📦 Project Modules & Flow

Here’s how your work is structured, moving from exploration to deployment:

| Module | Nickname | What It Does | Status |
|---|---|----------------|--------|
| **Temporal CPUE Analysis** | *The Navigation Course* | Time-series of squid catch (CPUE) across years, with environmental summaries and trend indicators | ✅ Complete |
| **CPUE Standardization & Predictive Modeling** | *Course Correction* | Normalize catch via GAM/GLM, compare prediction performance | ✅ Complete |
| **Biomass Forecasting + Environment** | *Ocean Dynamics* | Surplus production modeling including environmental drivers (SST, SSH, Chl‑a) | ✅ Complete |
| **AutoML / Predictive Catch Models** | *The Engine Room* | Automated modeling pipelines for daily/weekly catch | 🔄 In progress |
| **(Future) MLOps / Deployment + Versioning** | *Launch Control* | Model deployment, versioning, monitoring; experimental | 🧪 Planned |

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
- **Statistical & Predictive Modeling:** `pygam`, `statsmodels` (GAM, GLM, Tweedie)  
- **AutoML / Machine Learning:** `scikit-learn`, `PyCaret`  
- **Spatial & Dashboard Tools:** `folium`, `plotly`, `streamlit`  
- **Remote Sensing Processing:** extraction of Chlorophyll‑a and SSH from NetCDF layers  
- **Missing Data Imputation:** median of nearby spatial/temporal neighbors — chosen for stability across gaps and variable neighbor distributions  
- **Development Environment:** Jupyter Notebooks, VSCode  

---

## 📌 Data & Method Highlights

- Base dataset included: `catch_kg`, `longitude`, `latitude`, `vessel_id`, `SST`, `depth`, `year`, `month`, `day`  
- Augmented with satellite layers (Chlorophyll‑a, SSH) pulled from NASA / Copernicus portals  
- Missing environmental values imputed via median of local neighbors to mitigate influence of extreme values or sparse coverage  
- Modeling workflows:
  - GAMs, GLMs for CPUE normalization and prediction  
  - Environmentally dependent surplus production model for biomass forecasts  
  - AutoML experiments for short-term catch prediction  

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

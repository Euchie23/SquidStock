# 🌊 Ocean Dynamics — Environmentally Driven Biomass Simulation (warming scenarios)

## 📘 Executive Summary
This module simulates *Illex argentinus* biomass under **baseline and +2 °C warming scenarios** using an **Environmentally Dependent Surplus Production Model (EDSPM)**.  

**Key Findings:**
- **Short-term warming effect:** Early-season biomass (Jan–Mar) slightly increases, then converges back to baseline due to density dependence.  
- **CPUE vs Biomass:** Normalized CPUE is noisy and weakly correlated with actual biomass — catch rates reflect aggregation, effort, and gear efficiency rather than stock size.  
- **Management Insight:** Environment-aware indicators are more reliable than CPUE alone for seasonal quota and closure decisions.  
- **Data Scope:** Analysis focuses on **January–June** (20-year dataset).  

---

## 📈 Real-World Value
This module introduces **population-level environmental modeling** for cephalopods, bridging the gap between CPUE analysis and ecosystem-aware forecasting.  

**Who This Helps:**
- **Fisheries agencies:** test warming scenarios & evaluate stock resilience  
- **Climate adaptation teams:** understand stock response to environmental change  
- **Marine NGOs & policy groups:** support ecosystem-based management planning  
- **Research labs:** explore EDSPM-style modeling and uncertainty propagation  

**Why It Matters:**  
CPUE alone cannot track total abundance, especially for mobile, short-lived species like squid. EDSPM captures ecological limits, seasonality, and climate sensitivity to inform **adaptive management**.

---

## 🧩 Module Overview
**Core Objectives:**
- Build an **environmental index** (0.6·SST + 0.4·Chl-a)  
- Run **EDSPM** for baseline and +2 °C warming scenarios  
- Propagate uncertainty using **Monte Carlo simulations** (mean + 95% CI)  
- Compare normalized **biomass vs CPUE** indices  

**Outcome:** Provides actionable insights for **seasonal management, adaptive quotas, and climate resilience assessment**.

---

## 🧮 Model Specification

The Environmentally Dependent Surplus Production Model (EDSPM) modifies the classical logistic growth framework:

**Biomass dynamics**
```math
B_{t+1} = B_t + P_t - C_t
```

**Surplus production**
```math
P_t = r_t \, B_t \left(1 - \frac{B_t}{K}\right)
```

**Temperature-dependent growth**
```math
r_t = r_{\max} \exp\!\left( -\frac{(T_t - T_{opt})^2}{2\sigma_T^{\,2}} \right)
```

**Environmental index**
```math
E(t) = 0.6\,\widetilde{SST} + 0.4\,\widetilde{Chl}
```

Environmental conditions modulate growth over time  
(higher $E(t)$ → more favorable growth).


---

## 🔧 Default parameters (used in app & notebook)

| Parameter | Default value | Typical range | Meaning |
|---:|---:|---:|---|
| **K** | **5,000,000 tons** | 4–6 million | Ecosystem carrying capacity |
| **N₀** | **1,500,000 tons** | 1–4 million | Start-season biomass |
| **r₀ (r_max)** | **0.15 day⁻¹** | 0.015–0.30 | Max intrinsic growth |
| **Tₒₚₜ** | **12 °C** | 10–14 °C | Thermal optimum |
| **σₜ** | **3 °C** | 2–4 °C | Thermal sensitivity |
| **ΔT** | **+2.0 °C** | 0–4 °C | Warming scenario tested |
| **q** | **5e-5** | tuneable | Catchability (harvest efficiency) |

---


## 📊 Simulation & Visual Outputs 
> (saved under `../outputs/Biomass_Forecasting/`) <br>
> Scroll below for rendered outputs in "📸 Static Previews" section

| Visualization | Description | Output |
|----------------|--------------|---------|
| **Temperature-dependent Growth (EDSPM)** | Nonlinear SST–growth rate relationship | [`Temperature-Dependent Growth (EDSPM)`](https://github.com/Euchie23/SquidStock/blob/main/outputs/Biomass_Forecasting/temperature_dependent_growth_rate.png) |
| **Biomass Under Warming Scenarios** | Baseline vs. +2 °C trajectories | [`biomass_simulation (Panel 1)`](https://github.com/Euchie23/SquidStock/blob/main/outputs/Biomass_Forecasting/biomass_scenarios_comparison.png) |
| **% Change in Biomass** | Relative warming effect | `biomass_simulation (Panel 2)` |
| **Environmental Index E(t)** | Seasonality under baseline vs warming | `biomass_simulation (Panel 3)` |
| **CPUE vs Biomass** | Time Series | [`cpue_vs_biomass.png`](https://github.com/Euchie23/SquidStock/blob/main/outputs/Biomass_Forecasting/cpue_vs_biomass_comparison.png)|
| **CPUE vs Biomass** | Scatter Plot | [`cpue_vs_biomass_scatter_fig.png`](https://github.com/Euchie23/SquidStock/blob/main/outputs/Biomass_Forecasting/cpue_vs_biomass_scatter_fig.png)|

[See notebook for reference](https://github.com/Euchie23/SquidStock/blob/main/notebooks/Biomass_Forecasting/Biomass_Forecasting_Environment.ipynb).

---

## 🎯 Applied Use Case

**Scenario:** +2 °C warming  

- Early-season biomass (Jan–Mar) slightly increases, then returns to baseline due to density dependence  
- **Management implication:** Early CPUE boosts do **not** indicate sustainable stock growth  
- Use **environment-informed indicators** to guide seasonal closures, adaptive quotas, or survey timing

Interactive App: Explore biomass forecasting based on different scenarios in a concise, user-friendly interface: [Launch the App](https://squidstock-ocean-dynamics.streamlit.app)

---

## 🛠️ Tools & Techniques

**Core libraries:**  
`pandas`, `numpy`, `matplotlib`, `plotly`, `scipy`, `pygam`

**Methods implemented:**  
- Environmental data normalization
- Monte Carlo Simulations for uncertainty
- Nonlinear temperature-dependent modeling  
- Scenario-based biomass simulations  
- Climate sensitivity analysis  
- CPUE–biomass correlation diagnostics  

---

## 🛠️ How to Run This Notebook

1. Clone this repository. 
      -  git clone https://github.com/Euchie23/SquidStock.git
2. Ensure you have Python 3 installed. 

3. Install dependencies via pip:
      -  e.g., pip install pandas numpy matplotlib seaborn statsmodels pygam jupyter
        
4. Launch Jupyter Notebook and open /notebooks/Biomass_Forecasting_Environment.ipynb
   
5. Run cells sequentially to reproduce the analysis.
   
---

## 🔒 Data Confidentiality Notice  

This project uses a simulated and anonymized dataset modeled after patterns observed during my work as a part-time research assistant at National Taiwan University. It is designed exclusively for methodological demonstration and skill development in machine learning, fisheries analysis, and environmental data science. The dataset does not represent official assessments, and no confidential or proprietary information is included.


---

## 📉 Limitations & Future Work

- **Simplified climate forcing:**  
  Only +2 °C scenarios tested; future work should include full IPCC-aligned projections (e.g., SSP2-4.5, SSP5-8.5).  
- **No fishing feedback:**  
  Catch (Cₜ) treated as constant; future models should incorporate effort dynamics or adaptive harvest.  
- **E(t) linear composition:**  
  Future iterations could apply **PCA-derived weighting** or include **SSH, mixed-layer depth**, or **wind anomalies**.  
- **Spatial homogeneity:**  
  Model is non-spatial; a **spatiotemporal EDSPM** could reveal distributional shifts under climate forcing.  

---

## 🧭 Summary Statement

*Illex argentinus* populations show **climate sensitivity without instability** — a hallmark of resilient but responsive species.  
Under moderate warming, biomass gains are **short-lived**, CPUE decouples from true abundance, and environmental cycles strengthen but stay rhythmic.  
The EDSPM framework therefore provides a realistic, mechanistic basis for **forecasting squid productivity under changing ocean conditions.** 
In practice, this framework enables agencies and consultancies to stress-test seasonal management strategies under plausible climate scenarios before implementation, rather than reacting to CPUE signals after change has already occurred.

---


## 🤝 Collaboration & Contact

Contributions and extensions are welcome — especially from researchers working on **cephalopod ecology, stock assessment modeling, or environmental forecasting**.  

📬 [**Email**](mailto:euchiejnpierre@gmail.com) | [**LinkedIn**](https://linkedin.com/in/euchiejnpierre)  

---

## 📸 Static Previews

### **Temperature-Dependent Growth (EDSPM)**  
This curve defines how intrinsic population growth responds to temperature, peaking at the species’ thermal optimum and declining outside that range. It ensures the model responds realistically to warming scenarios rather than increasing growth indefinitely.
![Temperature-Dependent Growth (EDSPM)](https://github.com/Euchie23/SquidStock/blob/main/outputs/Biomass_Forecasting/temperature_dependent_growth_rate.png) <br><br>

### **Simulated Biomass Under Two Scenarios** 
Baseline vs +2 °C warming (Jan–Jun)  
*Shows short-lived biomass gains under warming that fade due to density dependence*
- **Panel 1 – Simulated Biomass Under Two Scenarios**
- **Panel 2 – % Change in Biomass Due to Warming**
- **Panel 3 – Environmental Effect Index E(t)**
![biomass_simulation](https://github.com/Euchie23/SquidStock/blob/main/outputs/Biomass_Forecasting/biomass_scenarios_comparison.png)<br><br>

 ### **CPUE vs Biomass Relationship (time series)** 
 - Normalized comparison
 - Key insight: CPUE fluctuates independently of biomass, especially during aggregation periods
![cpue_vs_biomass](https://github.com/Euchie23/SquidStock/blob/main/outputs/Biomass_Forecasting/cpue_vs_biomass_comparison.png)

### **CPUE vs Biomass Relationship (scatter plot)** 
- Weak correlation highlights decoupling
- Management implication: CPUE should not be used as a sole abundance proxy
![cpue_vs_biomass](https://github.com/Euchie23/SquidStock/blob/main/outputs/Biomass_Forecasting/cpue_vs_biomass_scatter_fig.png)


---

> 🦑 *Project 3 of the [SquidStock](https://github.com/Euchie23/SquidStock) series — advancing data-driven, climate-aware squid fishery modeling.* <br>
> 📌 This project is the continuation of [**Temporal_Catch_Analysis Module**](https://github.com/Euchie23/SquidStock/edit/main/notebooks/Temporal_Catch_Analysis/README.md) and [**CPUE_Standardization_&_Prediction (2000-2020**](https://github.com/Euchie23/SquidStock/tree/main/notebooks/CPUE_Standardization_%26_Prediction/README.md) 


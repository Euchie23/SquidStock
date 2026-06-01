# 🌊 Ocean Dynamics — Environmentally Driven Biomass Simulation (warming scenarios)

## 🧭 Problem Framing & Data Context
Building on **CPUE standardization** ([Course Correction](https://github.com/Euchie23/SquidStock/edit/main/notebooks/CPUE_Standardization_&_Prediction)), we now explore how environmental drivers shape *Illex argentinus* biomass. Standardized CPUE is a reliable index but **does not fully capture underlying population dynamics**—especially under climate change scenarios. This module uses an **Environmentally Dependent Surplus Production Model (EDSPM)** to link biomass dynamics with environmental forcing, providing **forward-looking insights for adaptive management**.

---

## 📘 Executive Summary
This module simulates *Illex argentinus* biomass under **baseline and +2 °C warming scenarios** using an **Environmentally Dependent Surplus Production Model (EDSPM)**.  

**Key Findings:**
- **Warming effect:** Under +2 °C warming, biomass remains mostly stable to slightly improved, with modest average gains and a small positive final difference relative to baseline. This reflects improved alignment with the modelled thermal optimum under current assumptions.  
- **CPUE vs Biomass:** Normalized CPUE may show weak or negative relationships with simulated biomass, highlighting that catch rates can be influenced by aggregation, fishing location, gear efficiency, and effort rather than stock size alone. 
- **Management Insight:** Environment-aware indicators are more reliable than CPUE alone for seasonal quota and closure decisions.  
- **Data Scope:** Analysis focuses on **January–June** (21-year dataset).
- **Model limitation:** The simulation assumes a single thermal optimum, but Illex argentinus exhibits stage-specific and spatial habitat use (warm spawning, cold feeding grounds), meaning temperature-only responses may oversimplify real ecological dynamics.

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
- Represent **environmental forcing through separate pathways**: SST controls temperature-dependent growth, while chlorophyll-a acts as a productivity modifier  
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
P_t = r_t \,​ E_{env,t}\,​ B_t \left(1 - \frac{B_t}{K}\right)
```
Here, $\(E_{env,t}\)$ represents a productivity modifier, mainly based on chlorophyll-a, while temperature effects are handled separately through $\(r_t\)$.

**Temperature-dependent growth**
```math
r_t = r_{\max} \exp\!\left( -\frac{(T_t - T_{opt})^2}{2\sigma_T^{\,2}} \right)
```

**Productivity modifier**
```math
E_{env,t} = 0.7 + 0.3 \times \widetilde{ChlA_t}
```

The productivity modifier represents food-availability support using chlorophyll-a. Temperature is not included here because SST already influences growth through $r_t$.

Thermal suitability index
``` math
S_t = \exp\left(-\frac{(T_t - T_{opt})^2}{2\sigma_T^2}\right)

```
The thermal suitability index is used for interpretation and visualization, showing how closely environmental conditions align with the modelled thermal optimum.


---

## 🔧 Default parameters (used in app & notebook)

| Parameter | Default value | Typical range | Meaning |
|---:|---:|---:|---|
| **K** | **5,000,000 tons** | 4–6 million | Ecosystem carrying capacity |
| **N₀** | **3,000,000 tons** | 1–4 million | Start-season biomass |
| **r₀ (r_max)** | **0.03 day⁻¹** | 0.015–0.30 | Max intrinsic growth |
| **Tₒₚₜ** | **12 °C** | 10–14 °C | Modelled thermal optimum used in the simplified temperature-growth response |
| **σₜ** | **3 °C** | 2–4 °C | Thermal sensitivity |
| **ΔT** | **+2.0 °C** | 0–4 °C | Warming scenario tested |
| **q** | **2e-4** | tuneable | Catchability (harvest efficiency) |

---


## 📊 Simulation & Visual Outputs 
> (saved under `../outputs/Biomass_Forecasting/`) <br>
> Scroll below for rendered outputs in "📸 Static Previews" section

| Visualization | Description | Output |
|----------------|--------------|---------|
| **Temperature-dependent Growth (EDSPM)** | Nonlinear SST–growth rate relationship | [`Temperature-Dependent Growth (EDSPM)`](https://github.com/Euchie23/SquidStock/blob/main/outputs/Biomass_Forecasting/temperature_dependent_growth_rate.png) |
| **Biomass Under Warming Scenarios** | Baseline vs. +2 °C trajectories | [`biomass_simulation (Panel 1)`](https://github.com/Euchie23/SquidStock/blob/main/outputs/Biomass_Forecasting/biomass_scenarios_comparison.png) |
| **% Change in Biomass** | Relative warming effect | `biomass_simulation (Panel 2)` |
| **Thermal Suitability Index & Effort** | Thermal suitability under warming alongside fishing effort | `biomass_simulation (Panel 3)` |
| **CPUE vs Biomass** | Time Series | [`cpue_vs_biomass.png`](https://github.com/Euchie23/SquidStock/blob/main/outputs/Biomass_Forecasting/cpue_vs_biomass_comparison.png)|
| **CPUE vs Biomass** | Scatter Plot | [`cpue_vs_biomass_scatter_fig.png`](https://github.com/Euchie23/SquidStock/blob/main/outputs/Biomass_Forecasting/cpue_vs_biomass_scatter_fig.png)|

[See notebook for reference](https://github.com/Euchie23/SquidStock/blob/main/notebooks/Biomass_Forecasting/Biomass_Forecasting_Environment.ipynb).

---

## 🎯 Applied Use Case

**Scenario:** +2 °C warming  

- Biomass remains mostly stable to slightly improved under +2 °C warming, with modest gains relative to baseline under the current model settings
- **Management implication:** Apparent gains under warming may reflect model structure rather than true ecological benefit
- Use environment-informed indicators cautiously, as temperature-only models may overestimate productivity gains

Interactive App: Explore biomass forecasting based on different scenarios in a concise, user-friendly interface: 

![Dashboard Screenshot](https://drive.google.com/uc?export=view&id=1IIvMyXS2a5iK9FwGZlOl39aEgAVoIIE4)<br>
[Launch the App](https://squidstock-ocean-dynamics.streamlit.app)

---

## 🛠️ Tools & Techniques

**Core libraries:**  
`pandas`, `numpy`, `matplotlib`, `plotly`, `scipy`, `pygam`

**Methods implemented:**  
- Environmental data normalization and separation of thermal suitability from productivity forcing
- Monte Carlo Simulations for uncertainty
- Nonlinear temperature-dependent modeling  
- Scenario-based biomass simulations  
- Climate sensitivity analysis  
- CPUE–biomass correlation diagnostics  

---

## 📉 Limitations & Future Work

> These simulations inform strategic management under climate stress, but assumptions and simplifications may impact operational decisions such as quota setting, survey timing, or risk assessment

- **Simplified climate forcing:**  
  Only +2 °C scenarios tested; future work should include full IPCC-aligned projections (e.g., SSP2-4.5, SSP5-8.5).  
- **Simplified fishing dynamics:**  
  Harvest is represented using catchability, fishing effort, and simulated biomass. However, fisher behavior, spatial targeting,
adaptive effort shifts, and management feedbacks are not explicitly modelled. 
- **Simplified productivity forcing:**  
  Chlorophyll-a is used as a proxy for productivity, while other habitat drivers such as SSH, mixed-layer depth, wind anomalies, prey   availability, and upwelling intensity are not explicitly modelled.
- **Spatial homogeneity:**  
  Model is non-spatial; a **spatiotemporal EDSPM** could reveal distributional shifts under climate forcing.
- **Single thermal optimum assumption:**
  The model assumes one optimal temperature for growth, but Illex argentinus exhibits stage-specific and spatial thermal preferences   (warm spawning vs cold feeding grounds), which are not captured.
- **No migration dynamics:**
  The species undergoes large-scale seasonal migrations between the Brazil and Malvinas currents; the model treats biomass as spatially fixed, potentially misrepresenting environmental effects.
- **No explicit productivity (upwelling) effects:**
  Cold, nutrient-rich waters enhance prey availability in reality, but the model links temperature directly to growth, potentially misclassifying productive cold habitats as suboptimal.  

---

## 🧭 Summary Statement

*Illex argentinus* populations show **climate sensitivity without instability** — a hallmark of resilient but responsive species.  
Under moderate warming, biomass increases in the model due to improved alignment with a thermal optimum; however, this response likely overestimates real-world benefits because key ecological processes (migration, spatial structure, and productivity gradients) are not explicitly represented.  
The EDSPM framework therefore provides a simplified but mechanistic basis for exploring squid productivity under changing ocean conditions.
In practice, this framework enables agencies and consultancies to stress-test seasonal management strategies under plausible climate scenarios before implementation, rather than reacting to CPUE signals after change has already occurred.

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

## 🤝 Collaboration & Contact

Contributions and extensions are welcome — especially from researchers, data scientists, fisheries experts or consultants working on **cephalopod/marine ecology, stock assessment modeling, or environmental forecasting**  

📬 [**Email**](mailto:euchiejnpierre@gmail.com) | [**LinkedIn**](https://linkedin.com/in/euchiejnpierre)  

---

## 📸 Static Previews

### **Temperature-Dependent Growth (EDSPM)**  
This plot shows the simulated biomass trajectory alongside the temperature-dependent growth rate $\(r_t\)$. Growth varies through time depending on how close SST is to the modelled thermal optimum. It ensures the model responds realistically to warming scenarios rather than increasing growth indefinitely.
![Temperature-Dependent Growth (EDSPM)](https://github.com/Euchie23/SquidStock/blob/main/outputs/Biomass_Forecasting/temperature_dependent_growth_rate.png) <br><br>

### **Simulated Biomass Under Two Scenarios** 
Baseline vs +2 °C warming (Jan–Jun)  
*Shows a modest positive biomass response under +2 °C warming, with thermal suitability and fishing effort shown alongside biomass change*
- **Panel 1 – Simulated Biomass Under Two Scenarios**
- **Panel 2 – % Change in Biomass Due to Warming**
- **Panel 3 – Thermal Suitability Index and Effort**
![biomass_simulation](https://github.com/Euchie23/SquidStock/blob/main/outputs/Biomass_Forecasting/biomass_scenarios_comparison.png)<br><br>

 ### **CPUE vs Biomass Relationship (time series)** 
 - Normalized comparison
 - Key insight: CPUE fluctuates independently of biomass, especially during aggregation periods
![cpue_vs_biomass](https://github.com/Euchie23/SquidStock/blob/main/outputs/Biomass_Forecasting/cpue_vs_biomass_comparison.png)

### **CPUE vs Biomass Relationship (scatter plot)** 
- Weak or negative correlation highlights potential decoupling between CPUE and simulated biomass
- Management implication: CPUE should not be used as a sole abundance proxy
![cpue_vs_biomass](https://github.com/Euchie23/SquidStock/blob/main/outputs/Biomass_Forecasting/cpue_vs_biomass_scatter_fig.png)


---

> 🦑 *Project 3 of the [SquidStock](https://github.com/Euchie23/SquidStock) series — advancing data-driven, climate-aware squid fishery modeling.* <br>
> 📌 This project is the continuation of [**Temporal_Catch_Analysis Module**](https://github.com/Euchie23/SquidStock/edit/main/notebooks/Temporal_Catch_Analysis/README.md) and [**CPUE_Standardization_&_Prediction (2000-2020)**](https://github.com/Euchie23/SquidStock/tree/main/notebooks/CPUE_Standardization_%26_Prediction/) <br>
[Click here for App](https://squidstock-course-correction.streamlit.app)


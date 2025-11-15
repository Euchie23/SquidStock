# 🌊 Ocean Dynamics — Environmentally Driven Biomass Simulation (warming scenarios)

This module implements an **Environmentally Dependent Surplus Production Model (EDSPM)** to show how *Illex argentinus* biomass responds to environmental variability (SST & chlorophyll-a) and a moderate warming scenario. Analysis focuses on **January–June** (20-year dataset) — the most consistent seasonal window.

It integrates insights from **CPUE-based models (Module 2)** and moves toward **ecosystem-aware simulation**, forming a key bridge between fishery-dependent and environment-driven population indicators.

---

## 📘 Executive Summary

- **What we did:** Linked temperature and productivity to a logistic surplus-production model, added fishing removals and Monte Carlo uncertainty, and compared baseline vs **+2 °C warming**.
- **Main outcome:** Warming gives a **small, short-lived** biomass boost during early months; long-term biomass returns toward the same equilibrium because of density dependence.
- **CPUE vs biomass:** Normalized CPUE is **volatile** and weakly correlated with biomass — CPUE reflects catchability, aggregation and effort, not necessarily total stock.
- **Why it matters:** Environment-aware indicators are more reliable than CPUE alone for detecting ecologically meaningful change and guiding seasonal management (closures, adaptive quotas).
- **Data scope:** Results apply to **Jan–Jun** only (20 years); full-year behaviour may differ.

**Key additions integrated:**  
- CPUE often **does not** reliably reflect true abundance during January–June; catch rates are influenced by movement, hotspots, and gear efficiency.  
- Actionable takeaways: use environment-informed indicators, consider seasonal closures, and adapt quotas/timing around key growth months.
  
---

## 🧩 Module Overview
### “Modeling Resilience Under Climate Pressure”

**Core Objectives:**
- Build an environmental index (0.6·SST + 0.4·Chl-a)  
- Run EDSPM baseline and +2 °C warming scenarios  
- Propagate uncertainty with Monte Carlo runs (mean + 95% CI)  
- Compare normalized biomass index vs CPUE index  

---

## 🧮 Model Specification

The **Environmentally Dependent Surplus Production Model (EDSPM)** modifies the classical logistic growth framework:

**Dynamics**
\[
B_{t+1} = B_t + P_t - C_t
\]

**Surplus production**
\[
P_t = r_t B_t \left(1 - \frac{B_t}{K}\right)
\]

**Temperature-dependent growth**
\[
r_t = r_{\max}\exp\!\left(-\frac{(T_t - T_{opt})^2}{2\sigma_T^2}\right)
\]

**Environmental index**
\[
E(t)=0.6\cdot\widetilde{SST} + 0.4\cdot\widetilde{Chl}
\]

Environmental conditions modulate growth over time (higher E → more favorable growth).

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

## 📈 What was simulated

- **Baseline:** observed Jan–Jun forcing (SST, Chl-a)  
- **Warming:** SST increased by +2 °C over the simulation window  
- **Uncertainty:** Monte Carlo repeats to produce mean trajectories and 95% CI  
- **Comparisons:** biomass (mean + CI), % change vs baseline, environmental index, and CPUE vs biomass (normalized indices)

---

# 🔬 Key Takeaways

- **Short-term:** Warming slightly increases early-season productivity (a few percent), but this effect fades.  
- **Long-term:** The population returns to equilibrium — density dependence prevents runaway growth.  
- **Seasonality:** Timing of seasons is unchanged; peaks become somewhat stronger under warming.  
- **CPUE vs biomass:** CPUE is noisy and often decoupled from biomass (gear/behaviour & hotspots matter).  
- **Management implication:** Favor environment-informed indicators for seasonal decisions (timing and quotas); don’t rely on CPUE alone.

---

## 📊 Outputs (saved under `../outputs/EDSPM/`)

| File | What it shows |
|---|---|
| `temperature_dependent_growth_rate.png` | Gaussian thermal response (rₜ vs SST) |
| `biomass_scenarios_comparison.png` | 3-panel: biomass (baseline vs warming), % change, EnvIndex + effort |
| `cpue_vs_biomass_comparison.png` | Normalized time series — CPUE vs biomass (correlation) |
| `cpue_vs_biomass_scatter_fig.png` | Scatter + trend line (CPUE vs biomass index) |
| `biomass_uncertainty_simulation.png` | Mean biomass ± 95% CI (Monte Carlo) |

---

## 🌎 Real-World Relevance

Short-lived cephalopods like *Illex argentinus* exhibit rapid adaptation but limited persistence under changing conditions.  
This module’s results illustrate **why CPUE-only assessments can be misleading** — and why ecosystem-based modeling is crucial.

**Applied insights:**
- Fisheries may experience **temporary catch boosts** under mild warming.  
- Long-term biomass remains stable due to **ecological ceilings**.  
- Environmental models (like EDSPM) better capture **true population resilience**.  
- Climate adaptation strategies should consider **variability and timing**, not just mean warming.  

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

## 📊 Visual Outputs

| Visualization | Description | Output |
|----------------|--------------|---------|
| **Temperature-dependent Growth (EDSPM)** | Nonlinear SST–growth rate relationship | [`Temperature-Dependent Growth (EDSPM)`](https://github.com/Euchie23/SquidStock/blob/main/outputs/Biomass_Forecasting/temperature_dependent_growth_rate.png) |
| **Biomass Under Warming Scenarios** | Baseline vs. +2 °C trajectories | [`biomass_simulation (Panel 1)`](https://github.com/Euchie23/SquidStock/blob/main/outputs/Biomass_Forecasting/biomass_scenarios_comparison.png) |
| **% Change in Biomass** | Relative warming effect | `biomass_simulation (Panel 2)` |
| **Environmental Index E(t)** | Seasonality under baseline vs warming | `biomass_simulation (Panel 3)` |
| **CPUE vs Biomass** | Decoupling | [`cpue_vs_biomass.png`](https://github.com/Euchie23/SquidStock/blob/main/outputs/Biomass_Forecasting/cpue_vs_biomass_comparison.png)|
| **CPUE vs Biomass** | Correlation | [`cpue_vs_biomass_scatter_fig.png`](https://github.com/Euchie23/SquidStock/blob/main/outputs/Biomass_Forecasting/cpue_vs_biomass_scatter_fig.png)|

[See notebook for reference](https://github.com/Euchie23/SquidStock/blob/main/notebooks/Biomass_Forecasting/Biomass_Forecasting_Environment.ipynb).

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

> *Illex argentinus* populations show **climate sensitivity without instability** — a hallmark of resilient but responsive species.  
>  
> Under moderate warming, biomass gains are **short-lived**, CPUE decouples from true abundance, and environmental cycles strengthen but stay rhythmic.  
>  
> The EDSPM framework therefore provides a realistic, mechanistic basis for **forecasting squid productivity under changing ocean conditions.**

---

## 🤝 Collaboration & Contact

Contributions and extensions are welcome — especially from researchers working on **cephalopod ecology, stock assessment modeling, or environmental forecasting**.  

📬 [**Email**](mailto:euchiejnpierre@gmail.com) | [**LinkedIn**](https://linkedin.com/in/euchiejnpierre)  
🧠 Explore more modules at [**SquidStock Repository**](https://github.com/Euchie23/SquidStock)

---

## 🔒 Data Disclaimer

This module uses **synthetic and interpolated environmental data** based on observed patterns for *Illex argentinus* in the Southwest Atlantic.  
It does not represent official stock assessment data and is intended for methodological demonstration and educational purposes only.

---

## 📸 Static Previews

### **Temperature-Dependent Growth (EDSPM)**  
![Temperature-Dependent Growth (EDSPM)](https://github.com/Euchie23/SquidStock/blob/main/outputs/Biomass_Forecasting/temperature_dependent_growth_rate.png) <br><br>

### **Simulated Biomass Under Two Scenarios**  
- **Panel 1 – Simulated Biomass Under Two Scenarios**
- **Panel 2 – % Change in Biomass Due to Warming**
- **Panel 3 – Environmental Effect Index E(t)**
![biomass_simulation](https://github.com/Euchie23/SquidStock/blob/main/outputs/Biomass_Forecasting/biomass_scenarios_comparison.png)<br><br>

 ### **CPUE vs Biomass Relationship (decoupling)**  
![cpue_vs_biomass](https://github.com/Euchie23/SquidStock/blob/main/outputs/Biomass_Forecasting/cpue_vs_biomass_comparison.png)

### **CPUE vs Biomass Relationship (correlation)**  
![cpue_vs_biomass](https://github.com/Euchie23/SquidStock/blob/main/outputs/Biomass_Forecasting/cpue_vs_biomass_scatter_fig.png)


---

> 🦑 *Project 3 of the SquidStock series — advancing data-driven, climate-aware squid fishery modeling.*


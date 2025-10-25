# 🌊 Ocean Dynamics — Environmentally Driven Biomass Simulation (warming scenarios)

This notebook expands the *SquidStock* analytical series by linking **Illex argentinus** population dynamics to environmental variability and climate scenarios.  
Using an **Environmentally Dependent Surplus Production Model (EDSPM)**, this module quantifies how sea temperature and primary productivity shape biomass growth, stability, and resilience under both baseline and warming conditions.

It integrates insights from **CPUE-based models (Module 2)** and moves toward **ecosystem-aware simulation**, forming a key bridge between fishery-dependent and environment-driven population indicators.

---

## 📘 Executive Summary

This module simulates the biomass trajectory of *Illex argentinus* under two temperature scenarios — baseline and +2 °C warming — using a **nonlinear EDSPM formulation**.  
Environmental variability (temperature and chlorophyll) is expressed through a composite **Environmental Effect Index (Eₜ)**, driving changes in population growth rate over time.

Key outcomes reveal that *Illex argentinus* biomass demonstrates **strong short-term sensitivity** to warming but **long-term resilience** due to density dependence and ecological feedbacks.  
Despite warming-induced fluctuations in early growth, the system stabilizes near carrying capacity, showing self-regulation typical of opportunistic cephalopods.

---

## 🧩 Module Overview
### “Modeling Resilience Under Climate Pressure”

**Core Objectives:**
1. Integrate environmental drivers (SST, Chl-a) into a dynamic biomass simulation model.  
2. Evaluate biomass responses under baseline vs. +2 °C warming scenarios.  
3. Examine short-term productivity shifts vs. long-term equilibrium behavior.  
4. Compare model-derived biomass trends with fishery-dependent CPUE indices.  

---

## 🧮 Model Specification

The **Environmentally Dependent Surplus Production Model (EDSPM)** modifies the classical logistic growth framework:

\[
\frac{dB_t}{dt} = r_t B_t \left(1 - \frac{B_t}{K}\right) - C_t
\]

where  
- \( B_t \): biomass at time t  
- \( r_t \): temperature-dependent growth rate  
- \( K \): carrying capacity  
- \( C_t \): catch (tons)

The growth rate varies nonlinearly with **Sea Surface Temperature (SST)** through a Gaussian thermal response:

\[
r_t = r_{max} \cdot \exp\left[-\frac{(T_t - T_{opt})^2}{2\sigma_T^2}\right]
\]

and the **environmental favorability index** combines SST and Chlorophyll-a:

\[
E(t) = 0.6 \cdot \text{SST}_{norm} + 0.4 \cdot \text{Chl-a}_{norm}
\]

This structure allows temperature and productivity to dynamically influence population growth over time.

---

## 📈 Simulation Design

| Parameter | Description | Value / Source |
|------------|-------------|----------------|
| \(r_{max}\) | Maximum intrinsic growth rate | 0.4 |
| \(K\) | Carrying capacity (tons) | 1000 |
| \(B_0\) | Initial biomass (tons) | 300 |
| \(ΔT\) | Warming increment | +2 °C |
| Time Horizon | 120 months | (10 years) |

Two scenarios were simulated:  
- **Baseline:** Current mean SST  
- **Warming:** SST + 2 °C increase  

Environmental forcing was represented by monthly \(E(t)\) oscillations reflecting typical seasonal cycles in SST and Chl-a.

---

## 🧠 Model Interpretations

### **Panel 1 – Simulated Biomass Under Two Scenarios**

Both trajectories start from ~300 t and stabilize near 1000 t.  
The warming case rises slightly faster (months 10–15) but converges later (~month 70).

📘 *Ecological meaning:*  
Warming accelerates early productivity, but **density-dependent limits** (food, space, competition) restore equilibrium.  
This demonstrates **short-term environmental sensitivity** but **long-term stability**.

🟢 *Simplified takeaway:*  
A warmer ocean gives squid a small head start — not a permanent advantage.

---

### **Panel 2 – % Change in Biomass Due to Warming**

The relative difference peaks at **+1.5% around month 25** and gradually fades to zero by month 100.

📘 *Ecological meaning:*  
Warming produces a **temporary biomass gain** that dissipates as the population saturates.  
Squid respond quickly to better conditions, but ecosystem limits prevent indefinite growth.

🟢 *Simplified takeaway:*  
Squid populations bounce, not boom, under moderate warming.

---

### **Panel 3 – Environmental Effect Index E(t)**

E(t) cycles seasonally, with slightly higher peaks under warming but no change in frequency.  
This indicates **strong environmental rhythm** — warmer years amplify intensity, not timing.

📘 *Ecological meaning:*  
Productivity pulses become sharper but remain predictable.  
Warming changes **how strong** the good years are, not **when** they occur.

🟢 *Simplified takeaway:*  
Seasons stay the same, just a bit stronger.

---

### **CPUE vs Biomass Correlation**

A weak negative correlation (**r = –0.17**) reveals **decoupling** between fishery catch rates and actual biomass.

- Biomass stabilizes upward, while CPUE fluctuates erratically.  
- Fishing success (CPUE) reflects **availability and behavior**, not abundance.  

📘 *Ecological implication:*  
Environmental factors (temperature, prey fields, migration) and fleet patterns distort the CPUE–biomass link.

🟢 *Simplified takeaway:*  
Big catches don’t always mean more squid — sometimes they’re just easier to find.

---

## 🌍 Key Takeaways

| **Aspect** | **Observation** | **Ecological Implication** |
|:------------|:----------------|:----------------------------|
| **Biomass stability** | Near-identical under warming and baseline | Density feedback buffers climate impact |
| **Early growth** | Short-term warming boost | Enhanced metabolism and recruitment |
| **Temperature effect** | Nonlinear; peak 8–14 °C | Defines optimal growth window |
| **E(t) variability** | Stronger peaks, same rhythm | Climate amplifies intensity, not timing |
| **CPUE–Biomass link** | Weak (r = –0.17) | Catch rates don’t reflect real abundance |
| **Long-term behavior** | Convergent equilibrium (~1000 t) | Population self-regulation through feedbacks |

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
| **CPUE vs Biomass** | Correlation and decoupling | [`cpue_vs_biomass.png`](https://github.com/Euchie23/SquidStock/blob/main/outputs/Biomass_Forecasting/cpue_vs_biomass_comparison.png)|

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

 ### **CPUE vs Biomass Relationship**  
![cpue_vs_biomass](https://github.com/Euchie23/SquidStock/blob/main/outputs/Biomass_Forecasting/cpue_vs_biomass_comparison.png)

---

> 🦑 *Project 3 of the SquidStock series — advancing data-driven, climate-aware squid fishery modeling.*


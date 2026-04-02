# 🐙 SquidStock – Decision-Support for Biomass Estimation & CPUE Interpretation

---

## Context & Problem Framing

Short-lived cephalopods like *Illex argentinus* exhibit high sensitivity to environmental conditions, including temperature, ocean currents, and productivity. Their populations fluctuate rapidly, making **Catch-per-Unit-Effort (CPUE) an unreliable direct measure of stock biomass** in some conditions.  

Fisheries managers face a critical challenge: they need to understand whether observed CPUE trends reflect **true biomass dynamics**, and how climate-related warming scenarios may affect productivity and stock sustainability.  

The Biomass Simulator within SquidStock addresses the key decision question:

> **When and how can CPUE be trusted as an indicator of squid abundance, and what are the ecological implications of environmental change?**  

By integrating mechanistic population modeling, warming scenarios, and sensitivity analyses, this tool translates complex ecological and fisheries data into actionable decision insights.  

---

## Analytical Approach & Methodology

**Validated metrics:**  
- Baseline biomass initialized at 3,000,000 tons  
- Fishing mortality modeled via catchability (q = 2 × 10⁻⁴)  
- Growth rates modeled relative to species’ thermal optimum (Topt = 12°C)  

**Limitations:**  
- Model assumes a **single thermal optimum**; real squid use different temperatures for spawning vs feeding  
- **No spatial structure** (e.g., Brazil vs Malvinas currents)  
- **No migration or productivity dynamics**  
- Simplified fishing dynamics (constant catchability and effort)  

**Scenarios & assumptions:**  
- **Baseline (No Warming):** current environmental conditions  
- **Moderate Warming (+2°C):** temperature shifts toward thermal optimum  

**Sensitivity analysis:**  
- Explored CPUE–biomass relationships  
- Assessed robustness under environmental index fluctuations  

**Key metrics:**  
- Biomass trajectory  
- Relative % change in biomass under warming  
- CPUE sensitivity  

---

## Key Findings

### Baseline Scenario (No Warming)

- **Gradual decline**: Biomass decreases from ~3.0M → ~2.7M tons despite low exploitation (~0.7%)  
- **Mechanism**: Growth slightly below intrinsic potential; fishing mortality accumulates over time  
- **Caveat**: Cold-water feeding areas may actually enhance productivity; model likely **overestimates decline**  

---

### Warming Scenario (+2°C)

- **Apparent biomass increase**: ~5.5% higher than baseline; ~10% higher at the end of simulation  
- **Mechanism**: Growth aligned closer to thermal optimum within the model framework  
- **Caveat**: Ignores real-world cold-water productivity, migration, and spatial heterogeneity; results represent an **upper-bound estimate**, not a direct prediction  

---

### Sensitivity Analysis (CPUE vs Biomass)

- CPUE shows a **weak correlation** with simulated biomass  
- Model limitations: No aggregation, migration, or habitat-driven catchability effects  
- Implication: CPUE alone can be misleading for operational decisions  

---

## Supporting Context: CPUE Standardization & Weekly Prediction

While the Biomass Simulator translates ecological dynamics into biomass projections, the **Course Correction app** provides standardized CPUE indices (2000–2020) that remove confounding effects of effort, seasonality, and zero catches. Together, these modules allow managers to assess whether observed CPUE signals broadly reflect underlying stock trends.

The **Engine Room weekly CPUE prediction app** adds an operational perspective by forecasting short-term CPUE regimes (Low / Medium / High) and detecting anomalies or feature drift. Although it does not simulate biomass directly, these weekly outputs help decision-makers:

- Identify periods where CPUE signals deviate from expected patterns, indicating potential ecological or operational anomalies.
- Contextualize biomass projections from the simulator by comparing expected abundance trends with observed or predicted CPUE regimes.
- Focus on regime-level trends and adaptive management decisions without overreacting to ephemeral weekly fluctuations.

**Integration across apps enables:**

- Validation of CPUE patterns against modeled biomass trends.
- Detection of potential over- or under-estimation in fishery-dependent observations.
- Scenario-informed management decisions under baseline or warming conditions.

---

## Lessons Learned / Insights

- **Decision-focused presentation is key:** Aligning biomass trajectories with CPUE trends clarifies when indices are reliable.  
- **Transparency builds trust:** Explicitly stating model simplifications and ecological assumptions ensures stakeholders understand uncertainty.  
- **Scenario analysis informs planning:** Comparing baseline vs warming highlights potential risks or upper-bound benefits.  
- **Integration with upstream CPUE data enhances context:** Standardized indices validate model projections and identify areas where CPUE misrepresents biomass.  

---

## Impact / Takeaways for Decision-Makers

- Provides **mechanistic insight into CPUE–biomass decoupling**, reducing reliance on raw CPUE trends alone.  
- Highlights **potential impacts of moderate warming** on squid productivity, while clearly indicating model limitations.  
- Supports **adaptive fisheries management** by combining scenario testing, sensitivity analysis, and CPUE validation.  
- Offers a **transparent, reproducible, scenario-driven framework** that informs quota setting, stock assessment, and climate-risk evaluation.

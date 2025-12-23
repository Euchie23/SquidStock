# 🧭 The Navigation Course — Temporal Catch Analysis

## 📘 Executive Summary
Temporal catch patterns reveal that squid catches are largely shaped by biological cycles and environmental conditions. Seasonal peaks from **March to June** align with migration and spawning behavior, while declining mean CPUE after 2015, alongside increasing water temperatures and deeper fishing depths, suggest that squid are shifting vertically and possibly experiencing stock stress, rather than changes being driven by fishing effort alone.

**Key Insights:**
- 🎣 **Seasonal Peaks:** March–June catches reflect migration and spawning cycles.  
- 📉 **Declining CPUE:** Mean catch decreases post-2015 indicate potential stock stress or reduced catch efficiency.  
- 🌡️ **Increasing Temperature:** Rising SST likely pushes squid to deeper or cooler waters.  
- ⏬ **Fishing Depth Increase:** Suggests vertical squid movement or adaptive fishing behavior.  

---

## 📈 Real-World Value
The Navigation Course provides a clear, **data-driven picture of how squid catch and ocean conditions have changed** over two decades.  

**Who This Helps:**
- **Fisheries scientists:** Understand baseline patterns before formal CPUE standardization  
- **Marine managers:** Detect early warning signs like declining CPUE or warming waters  
- **Sustainability teams:** Integrate long-term indicators into ecological reporting  

**Why It Matters:**  
Before building models or forecasts, managers need to understand what the raw data is telling them. This module **makes trends visible and interpretable**, forming a reliable foundation for sustainable stock management.

---

## 🗃️ Data & Modeling Overview
This notebook serves as the **first step in the analysis pipeline**, exploring temporal dynamics in *Illex argentinus* catch data (2000–2020). It introduces **clean, reproducible workflows** for later CPUE standardization and links trends to environmental drivers such as **Water Temperature** and **Fishing Depth**.

### Dataset Schema

| Column | Description | Type |
|--------|-------------|------|
| POINTID | Unique record identifier | Integer |
| CTNO | Catch trip number | Integer |
| Year, Month, Day | Temporal fields | Integer |
| Lon, Lat | Catch coordinates | Float |
| WaterTemp | Sea surface temperature (°C) | Float |
| Depth | Fishing depth (m) | Integer |
| SqCatch_Kg | Squid catch (kg) | Float |

---

## 📊 Key Results & Interpretation

### Temporal Patterns
- **Seasonality:** March–June peaks consistent across years  
- **Decline in mean CPUE:** Post-2015 trend suggests potential stock stress  
- **Environmental Drivers:** Rising SST and increasing fishing depth correspond to decreasing CPUE  

### Figures
- **Catch Time-Series Plot:** Seasonal trends and inter-annual variability  
  ![Catch Trend Plot](https://github.com/Euchie23/SquidStock/blob/main/outputs/Temporal_Catch_Analysis/monthly_catch_plot.png)  
- **Yearly Summary Table:** Environmental features with trend arrows  
  ![Yearly Summary Table](https://github.com/Euchie23/SquidStock/blob/main/outputs/Temporal_Catch_Analysis/yearly_feature_summary.png)
  > Arrow Key: Red ↑↓ = Negative/Unfavorable Trend | Green ↑↓ = Positive/Favorable Trend | Black → = Stable/No Change
- **Data Distribution Table:**  Catch data distribution throughout the 20 years  
  ![Data Distribution Summary](https://github.com/Euchie23/SquidStock/blob/main/outputs/Temporal_Catch_Analysis/data_distribution_summary.png) <br><br>


> 🔗 Viewing Interactive Plots
> (Works best on desktop or tablet in Chrome or Firefox)

> ✅ Option 1: View Online (Recommended)
> We’ve hosted the interactive plot via GitHub Pages for immediate viewing:

> 💾 Option 2: Download and Open Locally
> 📝 If the online version doesn’t load or you want to view offline:

> Navigate to the Temporal Catch Plot folder in this repo.
> Right-click the file → "Save link as..."
> Save the file to your computer and double-click to open in your browser (Chrome, Firefox, Edge).


---

## 🎯 Applied Use Case — Early Detection & Monitoring
**Objective:** Use raw catch and environmental data to detect trends, seasonality, and potential stress in squid stocks before formal modeling.  

**Supports:**  
- Early warning for stock stress  
- Identification of environmental changes affecting CPUE  
- Evidence-based planning for sustainable fisheries  

**Interactive App:** Explore trends and yearly summaries in a **concise, user-friendly interface**: [Launch the App](https://squidstock-course-correction.streamlit.app)  

---

## 📓 Notebook — Reproducibility & Interactive Exploration
This analysis is implemented in a **Jupyter notebook**:  

- **Exploration:** Temporal CPUE, environmental trends, seasonality  
- **Static Outputs:** PNG/PDF plots for reports  
- **Interactive Outputs:** Plotly HTML graphs for dynamic analysis  

[Click here to view Temporal Catch Analysis notebook](https://github.com/Euchie23/SquidStock/blob/main/notebooks/Temporal_Catch_Analysis/Temporal_Catch_Analysis.ipynb)

---

## 🛠️ How to Run This Notebook

This analysis is implemented in Jupyter notebooks using Python 3. Required libraries include:

```python
import pandas as pd
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
import os
```

To run the notebook locally:

1. Clone this repository. 

2. Ensure you have Python 3 installed. 

3. Install dependencies via pip:
      -  e.g., pip install pandas plotly numpy matplotlib seaborn jupyter
        
4. Launch Jupyter Notebook and open /notebooks/Temporal_Catch_Analysis.ipynb
   
5. Run cells sequentially to reproduce the analysis. 
   
---

## 🔒 Data Confidentiality Notice

This dataset is a simulated approximation of a real-world squid stock assessment dataset used during my tenure as a part-time research assistant at National Taiwan University. Although it closely resembles actual data, any interpretation or conclusions drawn here cannot be assumed to represent real conditions in the region. This project primarily demonstrates analytical methods, data processing workflows, and skill development in fisheries and environmental data science.

---

## 📉 Limitations and Future Work

- **Data Granularity and Inconsistencies:**  
  - The catch data is highly granular, collected per coordinate and date, with multiple vessel locations per day (5–10 points/day). However, data coverage is uneven; for example, only months 1–5 in 2000 have data, and 2001 may have months 1–6 and 12 with data, with incomplete weekly coverage. This irregularity poses challenges in continuous temporal analysis. 
    
- **Environmental Data Resolution:**  
  - Satellite-derived environmental data have inherent coarse spatial and temporal resolution, potentially masking small-scale oceanographic variations affecting squid distribution.

- **Future Work:**  
  - Plans include integrating expanding temporal coverage, and incorporating additional environmental drivers or fisheries data layers to improve model robustness.
    
---

## 🤝 Collaboration & Contact

This project welcomes feedback, collaboration, and contributions from experts in:
- Marine ecology and fisheries science  
- Environmental and marine data science  
- Predictive modeling and dashboard development  

Feel free to open an issue, submit a pull request, or contact me directly for access to private modules or collaborative opportunities.

---

## 📬 Connect

[**Email:**](mailto:euchiejnpierre@gmail.com) | [**LinkedIn:**](https://linkedin.com/in/euchiejnpierre)  

Thank you for exploring **SquidStock** — advancing sustainable squid fisheries through data transparency and ecological insight.

---

> 📁 For more on the times-series analysis and visualizations using the full dataset, see the **Temporal CPUE Analysis Module** in the [SquidStock](https://github.com/Euchie23/SquidStock).

# 🗺️ The Navigation Course — Temporal CPUE Analysis

## 📘 Executive Summary
This notebook serves as the **first step in the analysis pipeline**, aimed at understanding the structure, distribution, and temporal dynamics of the raw dataset before applying statistical models. It does so by exploring temporal dynamics in *Illex argentinus* catch data (2000–2020), and introduces clean, reproducible workflows to analyze Catch Per Unit Effort (CPUE), track inter-annual shifts, and link them to environmental drivers such as sea Water Temperature, and fishing depth.

Key insights include:

- 🎣 **Seasonal peaks** in squid CPUE consistently occur between **March and June**, reflecting biological migration and spawning cycles.
- 📉 Mean CPUE shows a **general decline after 2014**, indicating potential stock stress or reduced catch efficiency.
- 🌡️ **Water temperature** steadily increases over time, likely pushing squid into **cooler or deeper zones**.
- ⏬ **Fishing depth** has increased over time, pointing to possible **vertical movement** of squid or shifts in fishing behavior.
  
---

## 🧭 Module Overview: The Navigation Course

This module provides an **exploratory analysis** of raw squid CPUE and environmental data.  
It includes descriptive statistics, time-series plots, and yearly summary tables — forming the **analytical foundation** for later modeling and hypothesis testing.

> While originally scoped to include spatial maps, this module focuses solely on **temporal dynamics** to characterize long-term trends and seasonality.
---

## 🗃️ Data Schema

| Column         | Description                                          | Type        |
|----------------|------------------------------------------------------|-------------|
| POINTID        | Unique point identifier                              | Integer     |
| CTNO           | Catch trip number                                   | Integer     |
| Year           | Year of catch                                      | Integer     |
| Month          | Month of catch                                     | Integer     |
| Day            | Day of catch                                       | Integer     |
| Lon            | Longitude coordinate of catch location             | Float       |
| Lat            | Latitude coordinate of catch location              | Float       |
| WaterTemp      | Water temperature (°C) at catch location           | Float       |
| Depth          | Fishing depth (m)                                   | Integer     |
| SqCatch_Kg     | Squid catch weight (Kg)                             | Float       |

---

## 📊 Contents & Workflow

The notebook progresses as follows:

1. **Data Loading & Cleaning**  
   Import and preprocess catch and environmental data (CPUE, WaterTemp, SSH, Chlorophyll-a, Depth).

2. **Exploratory Data Analysis**  
   Visualization of CPUE trends across months and years with static and interactive plots.

3. **Summary Table with Trend Arrows**  
   A detailed yearly summary table shows mean, standard deviation, min, and max for environmental variables, augmented with arrows indicating year-over-year increases (↑), decreases (↓), or stability/initial record (→).

4. **Output Export**  
   Static plots and summary tables are saved as PDF files within the repository’s `/outputs` folder for sharing and inclusion in reports.

---

## 📈 Visualizations & Tables

Note: These static visualizations are saved as PNG or PDF files in `/outputs/`. You can click now to view them or quickly scroll down to the 📸 Screenshots section for a preview.

- **CPUE Trend Plots:** Show monthly and yearly variations in catch rates.
  - [Static monthly trend plot (PDF)](https://github.com/Euchie23/SquidStock/blob/main/outputs/Temporal_CPUE_Analysis/monthly_cpue_plot_static.pdf)  
  - Interactive monthly trend plot *(See ⚠️ Viewing Interactive HTML Plots section below)*

- **Summary Tables:** Present yearly environmental feature statistics with trend arrows and data distribution summaries:
  - [Yearly feature summary (PNG)](https://github.com/Euchie23/SquidStock/blob/main/outputs/Temporal_CPUE_Analysis/yearly_feature_summary.png)
    - ↑ means the value increased compared to the previous year.
    - ↓ means the value decreased compared to the previous year.
    - → means no change or first year (no previous data to compare).
    > *Arrow Color Key: Red ↑↓ = Negative/Unfavorable Trend | Green ↑↓ = Positive/Favorable Trend | Black → = Stable/No Change*
  - [Data distribution summary (PDF)](https://github.com/Euchie23/SquidStock/blob/main/outputs/Temporal_CPUE_Analysis/data_distribution_summary.pdf)

---

## ⚠️ Viewing Interactive HTML Plots (CPUE Analysis)

Interactive plots (e.g., Plotly graphs) are saved as `.html` files and **cannot be previewed directly on GitHub** due to file size limits.

### ✅ Option 1: View Online (Recommended)

We’ve hosted the interactive plot via GitHub Pages for immediate viewing:

🔗 [View Interactive CPUE Plot](https://euchie23.github.io/SquidStock/monthly_cpue_plot.html)  
*(Works best on desktop or tablet in Chrome or Firefox)*

### 💾 Option 2: Download and Open Locally

📝 If the online version doesn’t load or you want to view offline:

- Navigate to the [`Temporal CPUE Plot`](https://euchie23.github.io/SquidStock/monthly_cpue_plot.html) folder in this repo.
- Right-click the file → "Save link as..."
- Save the file to your computer and double-click to open in your browser (Chrome, Firefox, Edge).

---

## 🛠️ Tools, Skills & Techniques Demonstrated

This project highlights several key data science and environmental analytics techniques:

- **Data Cleaning & Transformation** using `pandas`, `numpy`
- **Interactive Visualization** with `plotly.express`
- **Static Plotting & Reporting** using `matplotlib`, `seaborn`, and PDF export
- **Time-Series Aggregation & Exploration** (monthly/yearly trends)
- **Data Interpretation in Ecological Contexts** (SSH, Water Temperature, Depth)
- **Jupyter Notebook Workflow Design** and reproducibility

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
        
4. Launch Jupyter Notebook and open /notebooks/Temporal_CPUE_Analysis.ipynb
   
5. Run cells sequentially to reproduce the analysis.

[Click here to view Temporal CPUE Analysis notebook](https://github.com/Euchie23/SquidStock/blob/main/notebooks/Temporal_CPUE_Analysis/Temporal_CPUE_Analysis.ipynb) 
   
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

## 🔒 Data Confidentiality Notice

This dataset is a simulated approximation of a real-world squid stock assessment dataset used during my tenure as a part-time research assistant at National Taiwan University. Although it closely resembles actual data, any interpretation or conclusions drawn here cannot be assumed to represent real conditions in the region. This project primarily demonstrates analytical methods, data processing workflows, and skill development in fisheries and environmental data science.


## 📸 Screenshots

**Figure 1:** CPUE time-series plot showing seasonal catch trends.  
![View Static Monthly CPUE Plot (PDF)](https://github.com/Euchie23/SquidStock/blob/main/outputs/Temporal_CPUE_Analysis/monthly_cpue_plot_static.png)  

---

**Figure 2:** Yearly summary table with trend arrows for environmental features.  
![Feature Summary Table](https://github.com/Euchie23/SquidStock/blob/main/outputs/Temporal_CPUE_Analysis/yearly_feature_summary.png)  

- ↑ means the value increased compared to the previous year.  
- ↓ means the value decreased compared to the previous year.  
- → means no change or first year (no previous data to compare).  
> *Arrow Color Key: Red ↑↓ = Negative/Unfavorable Trend | Green ↑↓ = Positive/Favorable Trend | Black → = Stable/No Change*
---

**Figure 3:** Yearly summary table showing data distribution throughout the 20 years.  
![View Data Distribution Summary (PDF)](https://github.com/Euchie23/SquidStock/blob/main/outputs/Temporal_CPUE_Analysis/data_distribution_summary.png)  

---

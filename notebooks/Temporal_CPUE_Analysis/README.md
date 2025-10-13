# 🦑 SquidStock — Temporal CPUE Analysis

## 📘 Executive Summary
This notebook establishes the analytical foundation for exploring temporal dynamics in *Illex argentinus* catch data (2000–2020). It introduces clean, reproducible workflows to analyze Catch Per Unit Effort (CPUE), track inter-annual shifts, and link them to environmental drivers such as sea Water Temperature, sea surface height (SSH), chlorophyll-a, and fishing depth.

Key insights include:

- 🎣 Seasonal peaks (March–June) dominate CPUE trends across years, with notable spikes in 2005 and 2014.
- 🌡️ Gradual ocean warming and declining chlorophyll levels suggest lower productivity in recent years.
- 🌊 Increased SSH variability and deeper mean fishing depths hint at changing oceanographic and squid behavioral patterns.
- 📉 Together, these indicators point to reduced biomass availability and potential climate-linked shifts in squid distribution.

This notebook forms the first module in the SquidStock series, supporting sustainable fisheries through transparent, data-driven marine analytics.

---

## 🧭 Module Overview: The Navigation Course (Catch & Temporal Exploration)
This module focuses on the exploration of squid catch time-series data and environmental variables, providing summary statistics and visualizations that uncover temporal patterns and trends. Although originally planned to include spatial maps, the current notebook version centers on time-series analysis and summary tables without interactive maps.

---

## 📂 Repository Structure

- `/notebooks` — Jupyter notebooks including The Navigation Course. Each notebook has its own README.md (like this one).  
- `/outputs` — Generated static plot PDFs and summary tables.  
- `/data` — Raw and processed datasets.


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
| SSH            | Sea Surface Height (m) at catch location           | Float       |
| Depth          | Fishing depth (m)                                   | Integer     |
| Chlor_a_mg_m3  | Chlorophyll-a concentration (mg/m³)                 | Float       |
| SqCatch_Kg     | Squid catch weight (Kg)                             | Float       |

---

## 🌐 Environmental Data Sources & Processing

Chlorophyll-a and SSH data were sourced from remote sensing platforms such as NASA MODIS and Copernicus Marine Service, using NetCDF files.

Monthly aggregates were derived based on the date and geolocation of each catch record.

### ⚠️ Handling Missing Environmental Data (Spatial Imputation)

For missing values (especially in remote areas or months with gaps), spatial imputation was applied:

If environmental data (e.g., SSH or chlorophyll) was unavailable at a given location, the nearest available value from surrounding coordinates within the same monthly window was used as a proxy.

This technique ensures continuity while maintaining reasonable geographic relevance.

ℹ️ Full spatial interpolation techniques (e.g., kriging, IDW) were **not used** due to computational constraints and the coarse resolution of satellite-derived data in this region.

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
  - [Static monthly trend plot (PDF)](https://github.com/Euchie23/SquidStock/blob/main/outputs/monthly_cpue_plot_static.pdf)  
  - Interactive monthly trend plot *(See ⚠️ Viewing Interactive HTML Plots section below)*

- **Summary Tables:** Present yearly environmental feature statistics with trend arrows and data summaries:
  - [Yearly feature summary (PNG)](https://github.com/Euchie23/SquidStock/blob/main/outputs/yearly_feature_summary.png)
    - ↑ means the value increased compared to the previous year.
    - ↓ means the value decreased compared to the previous year.
    - → means no change or first year (no previous data to compare).
  - [Data distribution summary (PDF)](https://github.com/Euchie23/SquidStock/blob/main/outputs/data_availability_summary.pdf)

---

## ⚠️ Viewing Interactive HTML Plots (CPUE Analysis)

Interactive plots (e.g., Plotly graphs) are saved as `.html` files and **cannot be previewed directly on GitHub** due to file size limits.

### ✅ Option 1: View Online (Recommended)

We’ve hosted the interactive plot via GitHub Pages for immediate viewing:

🔗 [View Interactive CPUE Plot](https://your-github-pages-link-here)  
*(Works best on desktop or tablet in Chrome or Firefox)*

### 💾 Option 2: Download and Open Locally

📝 If the online version doesn’t load or you want to view offline:

- Navigate to the `Temporal CPUE Plot` folder in this repo.
- Right-click the file → "Save link as..."
- Save the file to your computer and double-click to open in your browser (Chrome, Firefox, Edge).

---

## 🛠️ Tools, Skills & Techniques Demonstrated

This project highlights several key data science and environmental analytics techniques:

- **Data Cleaning & Transformation** using `pandas`, `numpy`
- **Interactive Visualization** with `plotly.express`
- **Static Plotting & Reporting** using `matplotlib`, `seaborn`, and PDF export
- **Time-Series Aggregation & Exploration** (monthly/yearly trends)
- **Spatial Imputation Logic** for environmental datasets using NetCDF files (`xarray`)
- **Remote Sensing Data Handling** (NASA MODIS, Copernicus)
- **Data Interpretation in Ecological Contexts** (SSH, SST, Chlorophyll-a analysis)
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

3. Install dependencies, e.g., via pip:
      - pip install pandas plotly numpy matplotlib seaborn jupyter
        
4. Launch Jupyter Notebook and open /notebooks/Temporal_CPUE_Analysis.ipynb
   
5. Run cells sequentially to reproduce the analysis.
   
---

## 📉 Limitations and Future Work

- **Data Granularity and Inconsistencies:**  
  - The catch data is highly granular, collected per coordinate and date, with multiple vessel locations per day (5–10 points/day). However, data coverage is uneven; for example, only months 1–5 in 2000 have data, and 2001 may have months 1–6 and 12 with data, with incomplete weekly coverage. This irregularity poses challenges in continuous temporal analysis. 

- **Spatial Imputation Constraints:**  
  - While nearest-neighbor spatial imputation was applied to fill missing environmental data, this method does not account for spatial autocorrelation or more complex spatial patterns. Full geostatistical methods (kriging, inverse distance weighting) were not feasible due to computational limits and coarse satellite data resolution.
    
- **Environmental Data Resolution:**  
  - Satellite-derived environmental data have inherent coarse spatial and temporal resolution, potentially masking small-scale oceanographic variations affecting squid distribution.

- **Future Work:**  
  - Plans include integrating more advanced spatial interpolation methods, expanding temporal coverage, and incorporating additional environmental drivers or fisheries data layers to improve model robustness.
    
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
![View Static Monthly CPUE Plot (PDF)](https://github.com/Euchie23/SquidStock/blob/main/outputs/monthly_cpue_plot_static.png)  

---

**Figure 2:** Yearly summary table with trend arrows for environmental features.  
![Feature Summary Table](https://github.com/Euchie23/SquidStock/blob/main/outputs/yearly_feature_summary.png)  

- ↑ means the value increased compared to the previous year.  
- ↓ means the value decreased compared to the previous year.  
- → means no change or first year (no previous data to compare).  

---

**Figure 3:** Yearly summary table showing data distribution throughout the 20 years.  
![View Data Distribution Summary (PDF)](https://github.com/Euchie23/SquidStock/blob/main/outputs/data_availability_summary.png)  

---

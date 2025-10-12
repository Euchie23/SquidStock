# 🦑 SquidStock — Temporal CPUE Analysis

## 📘 Executive Summary

This notebook establishes the analytical foundation for exploring temporal dynamics in *Illex argentinus* catch data (2000–2020). It introduces clean, reproducible workflows to analyze Catch Per Unit Effort (CPUE), track inter-annual shifts, and link them to environmental drivers such as sea surface temperature (SST), sea surface height (SSH), chlorophyll-a, and fishing depth.

**Key insights include:**

- 🎣 Seasonal peaks (March–June) dominate CPUE trends across years, with notable spikes in 2005 and 2014.
- 🌡️ Gradual ocean warming and declining chlorophyll levels suggest lower productivity in recent years.
- 🌊 Increased SSH variability and deeper mean fishing depths hint at changing oceanographic and behavioral patterns.
- 📉 Together, these indicators point to reduced biomass availability and potential climate-linked shifts in squid distribution.

This notebook forms the first module in the SquidStock series, supporting sustainable fisheries through transparent, data-driven marine analytics.

---

## 🧭 Module Overview: The Navigation Course (Catch & Temporal Exploration)

This module focuses on the exploration of squid catch time-series data and environmental variables, providing summary statistics and visualizations that uncover temporal patterns and trends. Although originally planned to include spatial maps, the current notebook version centers on time-series analysis and summary tables without interactive maps.

---

## 📊 Contents & Workflow

The notebook progresses as follows:

1. **Data Loading & Cleaning**  
   Import and preprocess catch and environmental data (CPUE, SST, SSH, Chlorophyll-a, Depth).

2. **Exploratory Data Analysis**  
   Visualization of CPUE trends across months and years with static and interactive plots.

3. **Summary Table with Trend Arrows**  
   A detailed yearly summary table shows mean, standard deviation, min, and max for environmental variables, augmented with arrows indicating year-over-year increases (↑), decreases (↓), or stability or initial record (→).

4. **Output Export**  
   Static plots and summary tables are saved as PDF files within the repository’s `/outputs` folder for sharing and inclusion in reports.

---

## 📂 Repository Structure

- /notebooks # Jupyter notebooks including The Navigation Course. each notebook has its own README.md (Like this one)
- /outputs # Generated static plot PDFs and summary tables
- /data # Raw and processed datasets

---

## 📈 Visualizations & Tables

> **Note:** These static visualizations are saved as png or pdf files in (`/outputs/`) you can click now to view them or quickly scroll down to the **📸 Screenshots** section for a preview .  
>  

- **CPUE Trend Plots:** Show monthly and yearly variations in catch rates.
  - [Static monthly trend plot (PDF)](https://github.com/Euchie23/SquidStock/blob/main/outputs/monthly_cpue_plot_static.pdf)  
  - Interactive monthly trend plot > *(See ⚠️ Viewing Interactive HTML Plots (CPUE Analysis) section below)* >

- **Summary Tables:** Present yearly environmental feature statistics with trend arrows and data summaries:
  - [Yearly feature summary (PNG)](https://github.com/Euchie23/SquidStock/blob/main/outputs/yearly_feature_summary.png)
    - ↑ means the value increased compared to the previous year.
    - ↓ means the value decreased compared to the previous year.
    - → means no change or first year (no previous data to compare).
  - [Data distribution summary (PDF)](https://github.com/Euchie23/SquidStock/blob/main/outputs/data_availability_summary.pdf)
    
---

## ⚠️ Viewing Interactive HTML Plots (CPUE Analysis)

Interactive plots (e.g., Plotly graphs) are saved as `.html` files and cannot be previewed directly on GitHub due to file size limits.

### ✅ Option 1: View Online (Recommended)

We’ve hosted the interactive plot via GitHub Pages for immediate viewing:

> 🔗 [**View Interactive CPUE Plot**](https://Euchie23.github.io/SquidStock/monthly_cpue_plot.html)  
> *(Works best on desktop or tablet in Chrome or Firefox)*

### 💾 Option 2: Download and Open Locally

> 📝 If the online version doesn’t load or you want to view offline:
>
> - Go to the [`/outputs`](https://github.com/Euchie23/SquidStock/blob/main/outputs/monthly_cpue_plot_static.html) folder in this repo.
> - Find the file: `monthly_cpue_plot.html`
> - Click the file → click **“Download”**, or:  
>   👉 Right-click **"View raw"** and choose **"Save link as..."**  
>   👉 Save the file to your computer and double-click it to open in your browser (Chrome, Firefox, Edge).


---

## 🤝 Collaboration & Contact

This project welcomes feedback, collaboration, and contributions from:

- Marine ecologists and fisheries scientists  
- Environmental data scientists  
- Predictive modelers and dashboard developers  

Feel free to open an issue, submit a pull request, or contact me directly for access to private modules or collaborative opportunities.

---

## 📬 Connect

- Email: [Euchie](mailto:euchiejnpierre@gmail.com)  
- LinkedIn: [Your LinkedIn Profile](https://linkedin.com/in/euchiejnpierre)  

Thank you for exploring SquidStock — advancing sustainable squid fisheries through data transparency and ecological insight.

---


## 📸 Screenshots

*Figure 1:* CPUE time-series plot showing seasonal catch trends.  
![CPUE Time-Series](https://github.com/Euchie23/SquidStock/blob/main/outputs/monthly_cpue_plot_static.pdf)

*Figure 2:* Yearly summary table with trend arrows for environmental features.  
![Feature Summary Table](https://github.com/Euchie23/SquidStock/blob/main/outputs/yearly_feature_summary.png)

*Figure 3:* Yearly summary table with showing data distribution througout the 20 years.  
![Distribution Summary Table](https://github.com/Euchie23/SquidStock/blob/main/outputs/data_availability_summary.pdf)

---
<img width="468" height="639" alt="image" src="https://github.com/user-attachments/assets/8316d640-b264-420a-a3e9-e327103e1d81" />


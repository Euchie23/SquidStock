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

/notebooks # Jupyter notebooks including The Navigation Course
/outputs # Generated static plot PDFs and summary tables
/data # Raw and processed datasets
README.md # This file

yaml
Copy code

---

## 📈 Visualizations & Tables

- **CPUE Trend Plots:** Show monthly and yearly variations in catch rates.  
- **Summary Table:** Presents yearly environmental feature statistics with arrows indicating trends:
  
  - ↑ means the value increased compared to the previous year.
  - ↓ means the value decreased compared to the previous year.
  - → means no change or first year (no previous data to compare).
  
> **Note:** These static visualizations are saved as PDF files (`/outputs/`) and committed to the repo for easy viewing.  
>  
> **Interactive plots** (e.g., plotly graphs) are included as HTML files but due to size limitations, GitHub cannot render them directly in the browser. To view them, please download and open locally.

---

## ⚠️ Viewing Interactive HTML Files on GitHub

GitHub cannot directly display large or complex HTML files in the browser. The interactive dashboards are included in the repo for completeness. Please:

- Download the HTML file(s) from the `/outputs` or `/interactive` folder.
- Open the file locally using a modern web browser (Chrome, Firefox, Edge).
  
Alternatively, consider hosting interactive dashboards via [GitHub Pages](https://pages.github.com/) or other services for online access.

---

## 🤝 Collaboration & Contact

This project welcomes feedback, collaboration, and contributions from:

- Marine ecologists and fisheries scientists  
- Environmental data scientists  
- Predictive modelers and dashboard developers  

Feel free to open an issue, submit a pull request, or contact me directly for access to private modules or collaborative opportunities.

---

## 📬 Connect

- Email: your.email@example.com  
- LinkedIn: [Your LinkedIn Profile](https://linkedin.com/in/yourprofile)  

Thank you for exploring SquidStock — advancing sustainable squid fisheries through data transparency and ecological insight.

---

<!-- Optional: Insert screenshots here -->

<!-- Example placement for screenshots: -->

## 📸 Screenshots

*Figure 1:* CPUE time-series plot showing seasonal catch trends.  
![CPUE Time-Series](./screenshots/cpue_timeseries.png)

*Figure 2:* Yearly summary table with trend arrows for environmental features.  
![Summary Table](./screenshots/summary_table.png)

---
<img width="468" height="639" alt="image" src="https://github.com/user-attachments/assets/8316d640-b264-420a-a3e9-e327103e1d81" />


# Project Samarth — Agri × Climate Q&A Prototype 🌾

**Developed by:** Swagath Somanna  
**Submission:** Project Samarth Internship Challenge

---

### 🎯 Overview
This project is a working prototype of an intelligent **Q&A system** that connects agricultural production data with climate indicators such as rainfall and temperature.  
It helps policymakers, researchers, and farmers ask natural questions and instantly get data-backed insights.

The project is inspired by **data.gov.in** datasets from:
- Ministry of Agriculture & Farmers Welfare  
- India Meteorological Department (IMD)

---

### ⚙️ Tech Stack
- **Python 3.12**
- **Streamlit** (for the front-end)
- **Pandas** (for data handling)
- **Matplotlib** (for visual insights)

---

### 🧠 Features
- Natural language question parsing (states, crops, years)
- Integrated datasets for rainfall, temperature, and crop production
- Auto-generated graphs and summaries
- Transparent data citations (each answer mentions its source)
- Extensible for live API integration with government datasets

---

### 🧩 How to Run Locally
1. Clone or download this project.
2. Open a terminal in the project folder.
3. Install dependencies:
   ```bash
   pip install streamlit pandas matplotlib
   ```
4. Run the app:
   ```bash
   streamlit run app.py
   ```
5. The app will open at [http://localhost:8501](http://localhost:8501).

---

### 💬 Example Questions
- “Compare the average annual rainfall in Karnataka and Maharashtra for the last 3 years.”  
- “List the top 3 crops produced in each state.”  
- “Analyze the rice production trend in Karnataka and its correlation with temperature.”

---

### 📊 Data Description
Representative datasets are included for demo purposes, based on open government data:
- **Rainfall data** — IMD historical data (2015–2021)
- **Crop production** — Ministry of Agriculture
- **Temperature trends** — IMD climate records

---

### 🚀 Future Scope
- Direct API integration with live data.gov.in datasets  
- Add district-level crop analysis  
- Include soil and groundwater data for more accurate modeling  

---



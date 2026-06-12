# 🌾 Tigray A-EWS - Kiremt 2026 Tabia-Level Drought Assessment

**Developer:** Yosef W. Kinfe | **Email:** Woyosef@caa.Columbia.edu / Woyosef@yahoo.com  
**Role:** Strategic Climate Systems Architect

---

## 📌 Overview

Tabia-level drought assessment system for Tigray region using EMI probabilistic forecasts and CHIRPS climate data.

**Key Features:**
- Tabia-level rainfall prediction (40+ Tabias)
- EMI tercile probability integration
- Percent of Normal calculation
- 5 drought categories / 4 response tiers
- Interactive Streamlit dashboard

---

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/Goitafa/Tigray-AEWS.git
cd Tigray-AEWS

# Install
pip install -r requirements.txt

# Run analysis
python scripts/01_tabia_rainfall_calculation.py
python scripts/02_tabia_weighted_probabilities.py

# Launch dashboard
streamlit run dashboard/streamlit_app.py

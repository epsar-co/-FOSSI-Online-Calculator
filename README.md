# -FOSSI-Online-Calculator
The **Fast Ossifier Stratification Index (FOSSI)** is a sex-specific risk stratification tool developed to identify individuals at risk of accelerated ossification in **diffuse idiopathic skeletal hyperostosis (DISH)**.   It was derived from the Fast Ossifier (FO) phenotype.  This repository hosts code and resources for the FOSSI Online Calculator.
Background
**DISH**: a common but often under-recognised condition marked by abnormal ligamentous ossification.  **Fast Ossifiers (FO)**: a subgroup of patients with rapid ossification and early trabecular decline.  
**FOSSI**: two indices, sex-specific, that capture the metabolic and inflammatory pathways driving accelerated disease.  
**FOSSI-F** (females) → insulin resistance–driven  
**FOSSI-M** (males) → inflammation/endocrine–driven  

Equations
**FOSSI-F (females):**
FOSSI_F = -18.811 + (0.209 × Age) + (0.350 × BMI) + (1.359 × CMI) + (0.799 × Hypertension) + (0.203 × VAI)

**FOSSI-M (males):**
FOSSI_M = -4.663 + (0.039 × Age) + (0.045 × BMI) – (0.223 × CMI) + (0.015 × WC)



---

## 🚀 Online Calculator
The easiest way to use FOSSI is via the **[FOSSI Online Calculator](https://epsar-co--fossi-online-calculator-app-1idwyr.streamlit.app/)** (Streamlit Cloud).  
👉 Input patient data and obtain FOSSI-F or FOSSI-M with risk categories.

---

💻 Local Installation

Clone the repo and install dependencies:

git clone https://github.com/epsar-co/fossi-calculator.git
cd fossi-calculator
pip install -r requirements.txt
streamlit run app.py


📜 License

Software code → MIT License

Documentation & example dataset → CC BY 4.0


📝 Citation

If you use this tool, please cite:

Pariente E, Martín-Millán M, Sgaramella G, et al.
‘Fast Ossifier’ in diffuse idiopathic skeletal hyperostosis: a sex-modulated, heterogeneous phenotype with accelerated ossification and early trabecular decline.
RMD Open. 2025;11:e006024. https://doi.org/10.1136/rmdopen-2025-006024


✉️ For questions or collaborations, please contact:
Emilio Pariente (MD, PhD) – emilio.pariente@scsalud.es


import streamlit as st

st.set_page_config(page_title="FOSSI Online Calculator", page_icon="🧮", layout="centered")

st.title("FOSSI Online Calculator")
st.caption("Fast Ossifier Stratification Index in Diffuse Idiopathic Skeletal Hyperostosis (DISH)")

st.markdown(
    """
**What is FOSSI?**  
FOSSI (Fast Ossifier Stratification Index) provides sex-specific risk stratification for accelerated ossification in DISH:
- **FOSSI-F (females)** - predominantly insulin resistance-driven
- **FOSSI-M (males)** - inflammation / endocrine-driven

This calculator implements the validated equations and thresholds described in the FOSSI manuscript.
"""
)

st.divider()

with st.expander("Input settings"):
    sex = st.selectbox("Sex", options=["Female", "Male"])
    col1, col2 = st.columns(2)
    age = col1.number_input("Age (years)", min_value=18, max_value=100, value=62, step=1)
    bmi = col2.number_input("BMI (kg/m²)", min_value=10.0, max_value=60.0, value=31.0, step=0.1, format="%.1f")

    col3, col4 = st.columns(2)
    height_cm = col3.number_input("Height (cm)", min_value=120.0, max_value=220.0, value=160.0, step=0.1, format="%.1f")
    wc_cm = col4.number_input("Waist circumference (cm)", min_value=50.0, max_value=180.0, value=98.0, step=0.1, format="%.1f")

    st.markdown("**Lipids unit**")
    unit = st.radio("Choose units for TG and HDL", options=["mmol/L", "mg/dL"], index=0, horizontal=True)

    col5, col6 = st.columns(2)
    tg = col5.number_input(f"Triglycerides (TG) ({unit})", min_value=0.1, max_value=20.0 if unit=="mmol/L" else 2000.0, value=1.9 if unit=="mmol/L" else 168.0, step=0.1, format="%.2f")
    hdl = col6.number_input(f"HDL cholesterol ({unit})", min_value=0.1, max_value=10.0 if unit=="mmol/L" else 400.0, value=1.0 if unit=="mmol/L" else 39.0, step=0.01, format="%.2f")

    ht = st.selectbox("Hypertension", options=["No (0)", "Yes (1)"], index=1)
    hypertension = 1 if "Yes" in ht else 0

# Unit conversion if needed
# mg/dL -> mmol/L conversions: TG: /88.57 ; HDL: /38.67
if unit == "mg/dL":
    tg_mmol = tg / 88.57
    hdl_mmol = hdl / 38.67
else:
    tg_mmol = tg
    hdl_mmol = hdl

# Derived indices
# CMI = [TG (mmol/L)/HDL (mmol/L)] × [WC (cm)/Height (cm)]
cmi = (tg_mmol / hdl_mmol) * (wc_cm / height_cm)

# VAI (females) = [WC / (36.58 + 1.89 × BMI)] × [TG/0.81] × [1.52/HDL]
vai = None
if sex == "Female":
    vai = (wc_cm / (36.58 + 1.89*bmi)) * (tg_mmol/0.81) * (1.52/hdl_mmol)

# FOSSI equations
# FOSSI-F = -18.811 + (0.209×Age) + (0.350×BMI) + (1.359×CMI) + (0.799×Hypertension) + (0.203×VAI)
# FOSSI-M = -4.663 + (0.039×Age) + (0.045×BMI) - (0.223×CMI) + (0.015×WC)
if sex == "Female":
    fossi = -18.811 + (0.209*age) + (0.350*bmi) + (1.359*cmi) + (0.799*hypertension) + (0.203*(vai if vai is not None else 0.0))
else:
    fossi = -4.663 + (0.039*age) + (0.045*bmi) - (0.223*cmi) + (0.015*wc_cm)

# Risk categorization & messaging
def format_number(x, dec=2):
    try:
        return f"{x:.{dec}f}"
    except Exception:
        return "—"

if sex == "Female":
    # thresholds: <5.84 low; 5.84–7.88 intermediate; 7.89–9.58 high; >9.58 very high
    if fossi < 5.84:
        risk_label, color, expl = "Low", "green", "Metabolically quiescent; FO prevalence ~12%."
    elif fossi <= 7.88:
        risk_label, color, expl = "Intermediate", "yellow", "Early metabolic priming; bone status variable."
    elif fossi <= 9.58:
        risk_label, color, expl = "High", "orange", "High-risk metabolic footprint; trabecular damage likely."
    else:
        risk_label, color, expl = "Very High", "red", "Near-certain FO; severe metabolic burden; trabecular deterioration."
else:
    # thresholds: <0.71 grey zone; >=0.71 high/very high
    if fossi < 0.71:
        risk_label, color, expl = "Grey zone (<0.71)", "yellow", "Baseline FO prevalence ~17%; monitor closely."
    else:
        risk_label, color, expl = "High/Very High (≥0.71)", "red", "Full FO phenotype; pronounced metabolic overload and trabecular decline."

st.divider()
st.subheader("Results")

# Color box
color_map = {"green":"#E8F5E9", "yellow":"#FFFDE7", "orange":"#FFF3E0", "red":"#FFEBEE"}
st.markdown(
    f"""
    <div style="padding:1rem;border-radius:12px;background:{color_map.get(color,'#F5F5F5')};border:1px solid #e0e0e0;">
    <b>FOSSI value:</b> {format_number(fossi,2)}<br/>
    <b>Risk category:</b> {risk_label}<br/>
    <i>{expl}</i>
    </div>
    """,
    unsafe_allow_html=True
)

with st.expander("Details and derived indices"):
    colA, colB = st.columns(2)
    colA.metric("CMI", format_number(cmi, 3))
    if sex == "Female":
        colB.metric("VAI (females)", format_number(vai, 3))
    else:
        colB.metric("Waist (cm)", format_number(wc_cm, 1))
    colC, colD = st.columns(2)
    colC.metric("TG (mmol/L)", format_number(tg_mmol, 3))
    colD.metric("HDL (mmol/L)", format_number(hdl_mmol, 3))

st.divider()

st.markdown(
    """
**Equation summary**  
- **FOSSI-F (females):** -18.811 + (0.209×Age) + (0.350×BMI) + (1.359×CMI) + (0.799×Hypertension) + (0.203×VAI)  
- **FOSSI-M (males):** -4.663 + (0.039×Age) + (0.045×BMI) - (0.223×CMI) + (0.015×WC)

**Thresholds**  
- **Women:** <5.84 (Low), 5.84–7.88 (Intermediate), 7.89–9.58 (High), >9.58 (Very High)  
- **Men:** <0.71 (Grey zone), ≥0.71 (High/Very High)

> **Unit note:** If you enter lipids in mg/dL, the app converts internally to mmol/L (TG ÷ 88.57; HDL ÷ 38.67).
"""
)

st.caption(
    "References: Pariente et al. 'Fast Ossifier' in DISH, RMD Open (2025) https://doi.org/10.1136/rmdopen-2025-006024; "
    "FOSSI manuscript (Sept 2025). This tool provides research-oriented risk stratification and "
    "does not replace clinical judgement. No data are transmitted off your browser in the Streamlit Cloud deployment."
)

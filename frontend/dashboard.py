import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Cyber Risk Dashboard", layout="wide")

st.title("Cyber Risk Quantification 📊")
st.write("Estimate financial risks based on security maturity, vulnerabilities, and industry threat levels.")

# User input fields
company_maturity = st.slider("Company Security Maturity (0-1)", 0.0, 1.0, 0.6)
num_vulnerabilities = st.number_input("Number of Open Vulnerabilities", min_value=0, value=10)
avg_exploitability = st.slider("Average Exploitability Score (0-10)", 0.0, 10.0, 7.5)
simulations = st.number_input("Number of Monte Carlo Simulations", min_value=100, max_value=10000, value=1000)

if st.button("Run Risk Simulation"):
    with st.spinner("Running Monte Carlo Simulation..."):
        # Send request to FastAPI
        response = requests.post(
            f"{API_URL}/monte-carlo-risk",
            json={
                "company_maturity": company_maturity,
                "num_vulnerabilities": num_vulnerabilities,
                "avg_exploitability": avg_exploitability
            },
            params={"simulations": simulations}
        )
        if response.status_code == 200:
            risk_data = response.json()
            st.success("Simulation Completed ✅")

            # Display Risk Metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("Mean Risk ($)", f"${risk_data['mean_risk']:,.2f}")
            col2.metric("95th Percentile Risk ($)", f"${risk_data['95th_percentile_risk']:,.2f}")
            col3.metric("Worst-Case Risk ($)", f"${risk_data['worst_case_risk']:,.2f}")

            # Visualization
            st.bar_chart({
                "Mean Risk": [risk_data["mean_risk"]],
                "95th Percentile Risk": [risk_data["95th_percentile_risk"]],
                "Worst-Case Risk": [risk_data["worst_case_risk"]]
            })
        else:
            st.error("Error in API request. Please check FastAPI server.")


from fastapi import FastAPI
from risk_model import RiskInput, calculate_risk
from backend.threat_api import get_cisa_threat_level
from backend.monte_carlo import monte_carlo_simulation

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Cyber Risk API is running!"}

@app.get("/threat-level")
def get_threat_level():
    return {"cisa_threat_count": get_cisa_threat_level()}

@app.post("/calculate-risk")
def get_risk(input_data: RiskInput):
    risk_result = calculate_risk(input_data)
    return risk_result

@app.post("/monte-carlo-risk")
def run_monte_carlo(input_data: RiskInput, simulations: int = 10000):
    """Runs Monte Carlo simulation for cyber risk estimation."""
    return monte_carlo_simulation(input_data, num_simulations=simulations)

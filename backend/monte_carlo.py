import numpy as np
from backend.risk_model import RiskInput, calculate_risk

def monte_carlo_simulation(input_data: RiskInput, num_simulations: int = 10000):
    """Runs Monte Carlo simulation to estimate financial risk."""
    
    risk_results = []
    
    for _ in range(num_simulations):
        # Introduce variability in exploitability and vulnerabilities
        varied_exploitability = np.random.normal(loc=input_data.avg_exploitability, scale=1.5)
        varied_vulnerabilities = np.random.normal(loc=input_data.num_vulnerabilities, scale=2)

        # Ensure values stay within realistic bounds
        varied_exploitability = max(0, min(10, varied_exploitability))
        varied_vulnerabilities = max(0, varied_vulnerabilities)

        # Create new input with random values
        simulated_input = RiskInput(
            company_maturity=input_data.company_maturity,
            num_vulnerabilities=int(varied_vulnerabilities),
            avg_exploitability=varied_exploitability
        )

        # Compute risk for this simulation
        risk_result = calculate_risk(simulated_input)
        risk_results.append(risk_result["estimated_risk"])

    # Calculate statistical insights
    mean_risk = np.mean(risk_results)
    percentile_95 = np.percentile(risk_results, 95)
    max_risk = np.max(risk_results)

    return {
        "mean_risk": round(mean_risk, 2),
        "95th_percentile_risk": round(percentile_95, 2),
        "worst_case_risk": round(max_risk, 2),
        "num_simulations": num_simulations
    }

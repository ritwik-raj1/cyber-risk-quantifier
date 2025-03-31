from pydantic import BaseModel
from backend.threat_api import get_cisa_threat_level

# Define input data structure
class RiskInput(BaseModel):
    company_maturity: float  # Security maturity score (0-1)
    num_vulnerabilities: int  # Count of open vulnerabilities
    avg_exploitability: float  # Avg exploitability score (0-10)

# FAIR-based risk calculation
def calculate_risk(data: RiskInput):
    # Get live threat intelligence data (CISA KEV)
    cisa_threat_count = get_cisa_threat_level()

    # Normalize threat level (Scale: 0.1 - 1.0 to avoid zero values)
    industry_threat_level = max(0.1, min(1.0, cisa_threat_count / 1000))  

    # Likelihood formula (FAIR approximation)
    likelihood = (data.avg_exploitability * 0.1) * (industry_threat_level) * (1 - data.company_maturity)

    # Ensure likelihood is never zero if vulnerabilities exist
    if data.num_vulnerabilities > 0:
        likelihood = max(likelihood, 0.01)  # Set a minimum threshold of 1% likelihood

    # Estimated financial impact ($50,000 per vulnerability)
    impact = data.num_vulnerabilities * 50000  

    # Risk score calculation
    risk_score = likelihood * impact  

    return {
        "likelihood": round(likelihood * 100, 2),  # Convert to percentage
        "impact": impact,
        "estimated_risk": round(risk_score, 2),
        "live_threat_level": cisa_threat_count
    }

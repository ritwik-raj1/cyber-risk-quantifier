import requests

# External threat intelligence sources
CISA_KEV_API = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"

def get_cisa_threat_level():
    """Fetches the latest CISA Known Exploited Vulnerabilities (KEV) threat count."""
    try:
        response = requests.get(CISA_KEV_API)
        if response.status_code == 200:
            data = response.json()
            return len(data.get("vulnerabilities", []))  # Count of known threats
        return 0
    except Exception as e:
        print(f"Error fetching CISA data: {e}")
        return 0

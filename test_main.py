import requests

BASE_URL = "http://127.0.0.1:8000"

# Sample case search values (replace with known values from your dataset)
SAMPLE_CASE = {
    "case_number": "DC/44/CC/15/2025",
    "complainant": "RAHUL BANSAL",
    "respondent": "MS TECH PLUS Through its AUTH REPRESENTATIVE",
    "complainant_advocate": "",  # optional
    "respondent_advocate": "",   # optional
    "industry_type": "FAILURE TO RESOLVE ISSUES",
    "judge": ""                  # optional
}

def test_states():
    print("Testing /states ...")
    resp = requests.get(f"{BASE_URL}/states")
    assert resp.status_code == 200, f"/states failed: {resp.status_code}"
    data = resp.json()
    print(f"✅ /states returned {len(data)} states")
    if data:
        print("Sample state:", data[0])
    return data

def test_commissions(states, test_state_name="ANDHRA PRADESH"):
    state_name = next((s['state_name'] for s in states if s['state_name'] == test_state_name), None)
    assert state_name, f"State '{test_state_name}' not found in /states"
    print(f"Testing /commissions/{state_name} ...")
    resp = requests.get(f"{BASE_URL}/commissions/{state_name}")
    assert resp.status_code == 200, f"/commissions/{state_name} failed: {resp.status_code}"
    data = resp.json()
    print(f"✅ /commissions/{state_name} returned {len(data)} commissions")
    if data:
        print("Sample commission:", data[0])
    return data, state_name

def test_cases_by_field(state_name, commission_name, field, value):
    endpoint = f"/cases/by-{field.replace('_','-')}"
    payload = {
        "state_name": state_name,
        "commission_name": commission_name,
        "search_value": value
    }
    print(f"Testing {endpoint} with search value '{value}' ...")
    resp = requests.post(f"{BASE_URL}{endpoint}", json=payload)
    assert resp.status_code == 200, f"{endpoint} failed: {resp.status_code}"
    data = resp.json()
    print(f"✅ {endpoint} returned {len(data)} cases")
    if data:
        print("Sample case:", data[0])
    return data

if __name__ == "__main__":
    print("Running Lexi Jagriti DCDRC API tests with live data...\n")

    # Test states endpoint
    states = test_states()

    # Test commissions endpoint
    commissions, state_name = test_commissions(states)
    commission_name = commissions[0]['commissionNameEn'] if commissions else state_name
    print(f"Using commission: {commission_name}\n")

    # Test all search fields from SAMPLE_CASE
    for field, value in SAMPLE_CASE.items():
        if value:  # skip empty values
            test_cases_by_field(state_name, commission_name, field, value)

    print("\nAll tests completed successfully!")

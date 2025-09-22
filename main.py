# main.py
from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel
import httpx

app = FastAPI(title="Lexi Jagriti DCDRC API")

# Jagriti base URL for case search
JAGRITI_BASE_URL = "https://e-jagriti.gov.in/services/case/caseFilingService/v2"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/115.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Referer": "https://e-jagriti.gov.in/",
    "Origin": "https://e-jagriti.gov.in",
}

SEARCH_TYPE_MAP = {
    "case_number": 1,
    "complainant": 2,
    "respondent": 3,
    "complainant_advocate": 4,
    "respondent_advocate": 5,
    "industry_type": 6,
    "judge": 7,
}

# --- Models ---
class State(BaseModel):
    state_id: int
    state_name: str

class Commission(BaseModel):
    commissionId: int
    commissionNameEn: str
    circuitAdditionBenchStatus: bool
    activeStatus: bool

# Request model for ID-based search
class CaseSearchByIdRequest(BaseModel):
    commissionId: int
    page: Optional[int] = 0
    size: Optional[int] = 30
    fromDate: Optional[str] = "2025-01-01"
    toDate: Optional[str] = "2025-09-22"
    dateRequestType: Optional[int] = 1
    serchType: int
    serchTypeValue: str
    judgeId: Optional[str] = ""

# Response model
class CaseResponse(BaseModel):
    case_number: str
    case_stage: str
    filing_date: str
    complainant: str
    complainant_advocate: Optional[str]
    respondent: str
    respondent_advocate: Optional[str]
    document_link: Optional[str]

# --- Utility Functions ---
async def fetch_cases_by_id(req: CaseSearchByIdRequest):
    payload = req.dict()
    async with httpx.AsyncClient(headers=HEADERS) as client:
        try:
            resp = await client.post(
                f"{JAGRITI_BASE_URL}/getCaseDetailsBySearchType",
                json=payload
            )
            resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=502, detail=f"Jagriti server error: {e.response.text}")

        data = resp.json().get("data", {}).get("content", [])
        cases = [
            CaseResponse(
                case_number=c.get("case_number", ""),
                case_stage=c.get("case_stage_name", ""),
                filing_date=c.get("case_filing_date", ""),
                complainant=c.get("complainant_name", ""),
                complainant_advocate=c.get("complainant_advocate_name"),
                respondent=c.get("respondent_name", ""),
                respondent_advocate=c.get("respondent_advocate_name"),
                document_link=c.get("document_link")
            )
            for c in data
        ]
        return cases

# --- Endpoints for states and commissions remain unchanged ---
@app.get("/states", response_model=List[State])
async def states():
    async with httpx.AsyncClient(headers=HEADERS) as client:
        resp = await client.get(f"https://e-jagriti.gov.in/services/report/report/getStateCommissionAndCircuitBench")
        resp.raise_for_status()
        data = resp.json().get("data", [])

    seen = set()
    states = []
    for item in data:
        name = item["commissionNameEn"].strip()
        if "CIRCUIT BENCH" in name or "BENCH" in name:
            continue
        if name not in seen:
            seen.add(name)
            states.append(State(state_id=item["commissionId"], state_name=name))
    return states

@app.get("/commissions/{state_name}", response_model=List[Commission])
async def commissions(state_name: str):
    async with httpx.AsyncClient(headers=HEADERS) as client:
        resp = await client.get(f"https://e-jagriti.gov.in/services/report/report/getStateCommissionAndCircuitBench")
        resp.raise_for_status()
        data = resp.json().get("data", [])

    commissions_list = [
        Commission(
            commissionId=item["commissionId"],
            commissionNameEn=item["commissionNameEn"],
            circuitAdditionBenchStatus=item.get("circuitAdditionBenchStatus", False),
            activeStatus=item.get("activeStatus", False)
        )
        for item in data
        if item["commissionNameEn"].upper().startswith(state_name.upper())
    ]

    if not commissions_list:
        raise HTTPException(status_code=404, detail="No commissions found for this state")
    return commissions_list

# --- ID-based Case Search Endpoints ---
@app.post("/cases/search")
async def search_cases(req: CaseSearchByIdRequest):
    payload = req.dict()
    print(payload)
    async with httpx.AsyncClient(headers=HEADERS) as client:
        try:
            resp = await client.post(
                f"{JAGRITI_BASE_URL}/getCaseDetailsBySearchType",
                json=payload
            )
            resp.raise_for_status()
            print(resp)
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=502, detail=f"Jagriti server error: {e.response.text}")
    
    # Return the full response as-is
    return resp.json()

# Lexi Jagriti DCDRC API

**Base URL:** `http://127.0.0.1:8000` (local development)

> **Note:** Instead of having multiple APIs for different case searches (by case number, complainant, respondent, etc.), this API has been simplified. You can now query Jagriti using **just one endpoint** `/cases/search` by providing the appropriate search type in the request.

---

## Quick Start

Follow these steps to run the API locally:

1. **Create a Python virtual environment:**
   ```bash
   python3 -m venv venv
   ```

2. **Activate the virtual environment:**
   ```bash
   # Linux / macOS
   source venv/bin/activate
   # Windows (PowerShell)
   venv\Scripts\Activate.ps1
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the FastAPI server with auto-reload:**
   ```bash
   uvicorn main:app --reload
   ```

5. **Test the API using `curl` commands** (examples below).

---

## Endpoints

### 1. Get All States

Retrieve all states available in the Jagriti system.

* **URL:** `/states`
* **Method:** `GET`
* **cURL Example:**
  ```bash
  curl 'http://127.0.0.1:8000/states' -X GET -H 'accept: application/json'
  ```

---

### 2. Get Commissions by State

Retrieve all commissions for a specific state.

* **URL:** `/commissions/{state_name}`
* **Method:** `GET`
* **cURL Example:**
  ```bash
  curl 'http://127.0.0.1:8000/commissions/DELHI' -X GET -H 'accept: application/json'
  ```

---

### 3. Search Cases by ID

Search cases based on commission ID and search type.

* **URL:** `/cases/search`
* **Method:** `POST`
* **Request Body Example:**
  ```json
  {
      "commissionId": 11000000,
      "page": 0,
      "size": 30,
      "fromDate": "2025-01-01",
      "toDate": "2025-09-22",
      "dateRequestType": 1,
      "serchType": 2,
      "serchTypeValue": "VARUN",
      "judgeId": ""
  }
  ```

* **cURL Example (Local API):**
  ```bash
  curl 'http://127.0.0.1:8000/cases/search' \
    -X POST \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
          "commissionId":11000000,
          "page":0,
          "size":30,
          "fromDate":"2025-01-01",
          "toDate":"2025-09-22",
          "dateRequestType":1,
          "serchType":2,
          "serchTypeValue":"VARUN",
          "judgeId":""
        }'
  ```

* **Response Example:**
  ```json
  {
      "message": "Case Detail successfully fetched.",
      "status": 200,
      "data": [
          {
              "case_number": "C123/2025",
              "case_stage": "ADMISSION",
              "filing_date": "2025-01-10",
              "complainant": "VARUN",
              "complainant_advocate": "A. Sharma",
              "respondent": "XYZ Ltd",
              "respondent_advocate": "B. Singh",
              "document_link": "https://e-jagriti.gov.in/doc/123"
          }
      ],
      "error": "false"
  }
  ```

---

## Notes

* `/cases/search` consolidates all previous case search endpoints into one. Simply change `serchType` to query by case number, complainant, respondent, advocate, judge, etc.
* Some searches may return an empty array depending on backend data and filters.
* Always ensure the FastAPI server is running before executing `curl` commands.
* Use this workflow: **create virtual environment → install dependencies → run server → use `curl` to query the API**.

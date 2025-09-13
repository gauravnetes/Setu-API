from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from data_loader import load_data_from_csv
from typing import List, Dict, Any

app = FastAPI (
    title="SETU (Bridge) API",
    description="A FHIR-compliant terminology service for AYUSH", 
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"], 
)

print("Server is starting, loading data...")
AYUSH_DB = load_data_from_csv('AYUSH_Data.csv')
print('-' * 20)

@app.get("/api/search", response_model=List[Dict[str, Any]])
async def search_terms(term: str = ""): 
    
    search_query = term.lower()
    
    if not search_query: 
        return []
    
    matches = []
    for traditional_term, data in AYUSH_DB.items(): 
        if search_query in traditional_term.lower(): 
            match_data = {
                "Traditional_Term": traditional_term, 
                "NAMASTE_Code": data['namaste_code'],
                "System": data['system'],
                "Modern_Name": data['modern_name'],
                "ICD11_TM2_Code": data['icd11_tm2'],
                "ICD11_Biomedicine_Code": data['icd11_biomed'],
                "Description": data['description']
            }
            matches.append(match_data)
            
    return matches

@app.get("/")
async def root(): 
    return {"message": "SETU (Bridge) API is running"}
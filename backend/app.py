from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from data_loader import load_data_from_csv
from typing import List, Dict, Any
from datetime import datetime, timezone

from fhir.resources.valueset import ValueSet, ValueSetExpansion, ValueSetExpansionContains
from fhir.resources.valueset import ValueSetComposeIncludeConceptDesignation
from fhir.resources.coding import Coding


# For Presentatoin
def remove_none_values(d: Any) -> Any:
    """
    Recursively remove all keys from a dictionary where the value is None.
    """
    if isinstance(d, dict):
        return {k: remove_none_values(v) for k, v in d.items() if v is not None}
    if isinstance(d, list):
        return [remove_none_values(v) for v in d]
    return d


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

@app.get("/api/search", response_model=ValueSet)
async def search_terms(term: str = ""): 
    
    search_query = term.lower()

    # ValueSet resource: 
    value_set = ValueSet(
        status="active", 
        url="http://sih.gov.in/fhir/ValueSet/namaste-icd-lookup", 
        name="NamasteIcdLookupValueSet"
    )
    
    
    if not search_query: 
        return value_set.model_dump()
    
    fhir_matches = []
    for traditional_term, data in AYUSH_DB.items(): 
        if search_query in traditional_term.lower(): 
            
            fhir_match = ValueSetExpansionContains(
                system="http://namaste.gov.in/codesystem", 
                code=data['namaste_code'], 
                display=traditional_term
            )
            
            designations = []
            
            designations.append(ValueSetComposeIncludeConceptDesignation(
                use={"code": "modern-name", "system": "http://setu-api.dev/CodeSystem/designation-use"},
                value=data['modern_name']
            ))
            designations.append(ValueSetComposeIncludeConceptDesignation(
                use={"code": "icd11-biomed-code", "system": "http://setu-api.dev/CodeSystem/designation-use"},
                value=data['icd11_biomed']
            ))
            designations.append(ValueSetComposeIncludeConceptDesignation(
                use={"code": "icd11-tm2-code", "system": "http://setu-api.dev/CodeSystem/designation-use"},
                value=data['icd11_tm2']
            ))
            designations.append(ValueSetComposeIncludeConceptDesignation(
                use={"code": "system", "system": "http://setu-api.dev/CodeSystem/designation-use"},
                value=data['system']
            ))
            designations.append(ValueSetComposeIncludeConceptDesignation(
                use={"code": "description", "system": "http://setu-api.dev/CodeSystem/designation-use"},
                value=data['description']
            ))
            
            fhir_match.designation = designations
            fhir_matches.append(fhir_match)
            
    current_timestamp = datetime.now(timezone.utc).isoformat()

    value_set.expansion = ValueSetExpansion(timestamp=current_timestamp, contains=fhir_matches)
                        
    return value_set


# For presentation 
@app.get("/clean-search", response_model=Dict[str, Any])
async def clean_search_terms(term: str = ""): 
    
    value_set_object = await search_terms(term)
    
    verbose_dict = value_set_object.model_dump()
    
    clean_dict = remove_none_values(verbose_dict)
    
    return clean_dict


@app.get("/")
async def root(): 
    return {"message": "SETU (Bridge) API is running"}



# {
#   "resourceType": "ValueSet",
#   "status": "active",
#   "url": "http://sih.gov.in/fhir/ValueSet/namaste-icd-lookup",
#   "expansion": {
#     "contains": [
#       {
#         "system": "http://namaste.gov.in/codesystem",
#         "code": "NAM-SK01-01",
#         "display": "Ardhavabhedaka",
#         "designation": [
#           {
#             "use": { // This tells you what the value is
#               "code": "modern-name",
#               "system": "http://setu-api.dev/CodeSystem/designation-use"
#             },
#             "value": "Migraine without aura"
#           },
#           {
#             "use": { // This tells you what the value is
#               "code": "icd11-biomed-code",
#               "system": "http://setu-api.dev/CodeSystem/designation-use"
#             },
#             "value": "8A80.0" 
#           },
#           {
#             "use": { // This tells you what the value is
#               "code": "icd11-tm2-code",
#               "system": "http://setu-api.dev/CodeSystem/designation-use"
#             },
#             "value": "SK01.0" 
#           }
#         ]
#       }
#     ]
#   }
# }
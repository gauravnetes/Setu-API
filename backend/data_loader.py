import pandas as pd 

def load_data_from_csv(path: str) -> dict: 
    
    db = {}
    
    try: 
        df = pd.read_csv(path)
        for row in df.itertuples(index=False): 
            db[row.Traditional_Term] = {
                "namaste_code": row.NAMASTE_Code, 
                "system": row.System, 
                "modern_name": row.Modern_Name,
                "icd11_tm2": row.ICD11_TM2_Code, 
                "icd11_biomed": row.ICD11_Biomedicine_Code,  
                "description": row.Description
            }
            
        print(f"Successfully loaded {len(db)} terms into memroy.")
        return db
    
    except FileNotFoundError: 
        print(f"Error: Data file not Found at {path}")
        return {}
    except Exception as e: 
        print(f"Error: An Error occured while loading data: {e}")
        return {}
    
    
    
# saving in { key: value } pair. 
# key: Traditional_Term: "Kampavata"
# value: Another Dictionary containing all the other information from that row. 
# result -> 

# AYUSH_DB = {
#     "Ardhavabhedaka": {
#         "namaste_code": "NAM-SK01-01",
#         "system": "Ayurveda",
#         "modern_name": "Migraine without aura",
#     },
#     "Kampavata": {
#         "namaste_code": "NAM-SK52-01",
#         "system": "Ayurveda",
#         "modern_name": "Parkinson's disease",
#         "icd11_tm2": "SK52.2",
#         "icd11_biomed": "8A01.Y",
#         "description": "Involuntary shaking or tremors..."
#     },
# }
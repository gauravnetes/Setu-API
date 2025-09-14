export interface SearchResult {
  NAMASTE_Code: string;
  Traditional_Term: string;
  System: string;
  Modern_Name: string;
  Description: string;
  ICD11_TM2_Code: string;
  ICD11_Biomedicine_Code: string;
}

export interface Diagnosis {
  Traditional_Term?: string;   // optional
  SETU_Link?: string;          // optional
  [key: string]: unknown;      // if there are other fields
}
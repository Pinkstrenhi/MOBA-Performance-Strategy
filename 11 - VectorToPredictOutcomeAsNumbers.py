import os 
import pandas as pd 

source = "D:/VectorToPredictOutcome/"
directoryToSave = "D:/VectorToPredictOutcomeAsNumbers/"

mapping = {
            "Low": 0,
            "Average": 1,
            "High": 2
          }

for league in os.listdir(source):
    leaguePath = os.path.join(source, league)
    
    leagueToSave = os.path.join(directoryToSave, league)
    os.makedirs(leagueToSave, exist_ok=True)
    
    for year in os.listdir(leaguePath):
        yearPath = os.path.join(leaguePath, year)
        
        yearToSave = os.path.join(leagueToSave, year)
        os.makedirs(yearToSave, exist_ok=True)
        
        for split in os.listdir(yearPath):
            splitPath = os.path.join(yearPath, split)
            
            splitToSave = os.path.join(yearToSave, split)
            os.makedirs(splitToSave, exist_ok=True)
            
            for file in os.listdir(splitPath):
                filePath = os.path.join(splitPath, file)
            
                df = pd.read_csv(filePath, encoding = "utf-16")
                
                df = df.replace(mapping)
                
                csvPath = os.path.join(splitToSave, f"{league}_{year}_{split}.csv")
                
                df.to_csv(os.path.join(splitToSave, csvPath), index=False, encoding="utf-16")
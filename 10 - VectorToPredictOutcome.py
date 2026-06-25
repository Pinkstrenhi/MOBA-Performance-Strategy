import os 
import csv
import pandas as pd 

def CreateCSV(filePath, fieldnames):
    with open(filePath, mode="w", encoding="utf-16", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)


def UpdateCSV(csvPath, write):
    with open(csvPath, mode="a", encoding="utf-16", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(write)

sourceCommitment = "D:/VotingClassifier/"
sourceCompliance = "D:/CompliancePercent/"

directoryToSave = "D:/VectorToPredictOutcome/"

tasks = ["assists", "barons", "controlwardsbought", "damagetochampions", "damagetotowers", "deaths", "earnedgold", 
         "inhibitors", "kills", "minionkills", "monsterkills", "opp_barons", "opp_inhibitors", "total cs", 
         "visionscore", "wardskilled", "wardsplaced"]
columnsID = ["playername", "teamname", "role",  "week", "result"]

allColumns = columnsID + tasks + ["compliance"]

for league in os.listdir(sourceCommitment):
    leaguePath = os.path.join(sourceCommitment, league)
    
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
            
            splitData = {}
            
            csvPath = os.path.join(splitToSave, f"{league}_{year}_{split}.csv")
                                    
            for role in os.listdir(splitPath):
                rolePath = os.path.join(splitPath, role)
                
                for task in os.listdir(rolePath):
                    taskPath = os.path.join(rolePath, task)
                    
                    for week in os.listdir(taskPath):
                        weekPath = os.path.join(taskPath, week)
                        
                        weekNumber = week.split("_")[1]
                        
                        dfCommitment = pd.read_csv(weekPath, encoding = "utf-16")
                        
                        compliancePath = os.path.join(
                                                        sourceCompliance, 
                                                        league, 
                                                        year, 
                                                        split, 
                                                        role, 
                                                        f"week_{weekNumber}.csv"
                                                     )
                        dfCompliance = pd.read_csv(compliancePath, encoding = "utf-16")
                        
                        getCompliance = {
                                                (row["playername"], row["teamname"]): row["compliancePercent"]
                                                for _, row in dfCompliance.iterrows()
                                        }
                        
                        for _, row in dfCommitment.iterrows():
                            
                            key = (row["playername"], row["teamname"], role, weekNumber)
                            
                            if key not in splitData:
                                
                                splitData[key] = {
                                                    "playername": row["playername"],
                                                    "teamname": row["teamname"],
                                                    "role": role,
                                                    "week": weekNumber,
                                                    "result": row["result"], 
                                                    "compliance": getCompliance.get(
                                                                                    (row["playername"], 
                                                                                     row["teamname"]),
                                                                                    None)
                                                 }
                                
                                for taskName in tasks:
                                    splitData[key][taskName] = None
                            splitData[key][task] = row["ensemble"]
            
            dfFinal = pd.DataFrame(splitData.values())
            dfFinal = dfFinal[allColumns]
            
            dfFinal.to_csv(csvPath, index=False, encoding="utf-16")
                        
                
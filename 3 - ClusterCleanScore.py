import os
import pandas as pd

source = "D:/Cluster/"
directoryToSave = "D:/ClusterCleanScore/"

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
            
            for role in os.listdir(splitPath):
                rolePath = os.path.join(splitPath, role)
                
                roleToSave = os.path.join(splitToSave, role)
                os.makedirs(roleToSave, exist_ok=True)
                
                for task in os.listdir(rolePath):
                    taskPath = os.path.join(rolePath, task)
                    
                    taskToSave = os.path.join(roleToSave, task)
                    os.makedirs(taskToSave, exist_ok=True)
                    
                    for week in os.listdir(taskPath):
                        weekPath = os.path.join(taskPath, week)
                        
                        
                        df = pd.read_csv(weekPath, encoding = "utf-16")
                        
                        if {"scoreMin", "scoreMax"}.issubset(df.columns):
                            if ((df["scoreMin"] == 0) & (df["scoreMax"] == 0)).all():
                                continue 
                            
                        clustersColumn = set(df["cluster"].unique())

                        if clustersColumn != {0, 1, 2}:
                            continue

                        weekToSave = os.path.join(taskToSave, week)
                        df.to_csv(weekToSave, encoding="utf-16", index=False)    
                                

                        
import os
import csv
import pandas as pd

def CreateCSV(filePath,fieldnames):
    with open(filePath, mode="w",encoding="utf-16", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)
def UpdateCSV(csvPath,write):
    with open(csvPath, mode="a",encoding="utf-16", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(write)

source = "D:/ClusterCleanScore/"
directoryToSave = "D:/ClusterLabel/"

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
                        
                        meanScore = (df.groupby("cluster")["scoreMax"].mean().sort_values())

                        labels = {}

                        if len(meanScore) == 3:
                            clusters_sorted = meanScore.index.tolist()
                            labels[clusters_sorted[0]] = "Low"
                            labels[clusters_sorted[1]] = "Average"
                            labels[clusters_sorted[2]] = "High"
            

                        df["label"] = df["cluster"].map(labels)

                        weekToSave = os.path.join(taskToSave, week)
                        df.to_csv(weekToSave, encoding="utf-16", index=False)
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
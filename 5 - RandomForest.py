import os
import csv
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

def CreateCSV(filePath,fieldnames):
    with open(filePath, mode="w",encoding="utf-16", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)
def UpdateCSV(csvPath,write):
    with open(csvPath, mode="a",encoding="utf-16", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(write)

source = "D:/ClusterLabel/"
directoryToSave = "D:/RandomForest/"

features = ["matches", "scoreMin", "scoreMax", "delta"]
target = "label"

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
                        try:
                            X = df[features]
                            y = df[target]
    
                            model = RandomForestClassifier()
                            model.fit(X, y)
    
                            df["classifier"] = model.predict(X)
    
                            savePath = os.path.join(taskToSave, week)
                            df.to_csv(savePath, encoding="utf-16", index=False)

                        except ValueError as e:
                            print(f"File Error -> {weekPath}")
                            print(f"Message -> {e}")
                                            
                        
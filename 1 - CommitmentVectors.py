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

source = "D:/PerRoleTaskAssociation/"
directoryToSave = "D:/CommitmentVectors/"

columnsID = ["gameid", "playername", "teamname", "result"]
fieldnames = ["playername","teamname","result","matches","scoreMin","scoreMax","delta"]

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
                
                for file in os.listdir(rolePath):
                    filePath = os.path.join(rolePath, file)
                    
                    fileName = file.split(".")[0]
                    
                    df = pd.read_csv(filePath, encoding="utf-16")
                    
                    tasks = [columns for columns in df.columns if columns not in columnsID]

                    for task in tasks:                        
                        taskTosave = os.path.join(roleToSave, task)
                        os.makedirs(taskTosave, exist_ok=True)
                        
                        taskPath = os.path.join(taskTosave, f"{fileName}_{task}.csv")
                        
                        CreateCSV(taskPath, fieldnames)

                        vector = (
                            df
                            .groupby(["playername", "teamname"])[task]
                            .agg(
                                matches="count",
                                scoreMin="min",
                                scoreMax="max"
                            )
                            .reset_index()
                        )

                        scoreMaxIndex = (df.groupby(["playername", "teamname"])[task].idxmax())
                        scoreMaxresult = (df.loc[scoreMaxIndex, ["playername", "teamname", "result"]])

                        grouped = vector.merge(scoreMaxresult, on=["playername", "teamname"], how="left")

                        grouped["delta"] = grouped["scoreMax"] - grouped["scoreMin"]

                        for _, row in grouped.iterrows():
                            UpdateCSV(
                                taskPath,
                                [
                                    row["playername"],
                                    row["teamname"],
                                    row["result"],
                                    int(row["matches"]),
                                    row["scoreMin"],
                                    row["scoreMax"],
                                    row["delta"]
                                ]
                            )

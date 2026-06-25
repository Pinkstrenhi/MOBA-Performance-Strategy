import os
import pandas as pd

source = "D:/ComplianceScores/"
directoryToSave = "D:/CompliancePercent/"

columnsID = ["playername", "teamname"]

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

                weekJoin = {}

                for task in os.listdir(rolePath):
                    taskPath = os.path.join(rolePath, task)

                    for weekFile in os.listdir(taskPath):
                        weekPath = os.path.join(taskPath, weekFile)

                        weekNumber = "_".join(weekFile.split("_")[:2])

                        df = pd.read_csv(weekPath)
                        df = df[columnsID + ["compliancescore"]]
                        df = df.rename(columns={"compliancescore": task})

                        if weekNumber not in weekJoin:
                            weekJoin[weekNumber] = df
                        else:
                            weekJoin[weekNumber] = weekJoin[weekNumber].merge(df,on=columnsID,how="outer")

                for weekNumber, dfWeek in weekJoin.items():

                    tasksColumns = [c for c in dfWeek.columns if c not in columnsID]
                
                    dfWeek["compliance"] = dfWeek[tasksColumns].mean(axis=1)
                
                    dfWeek["compliancePercent"] = (dfWeek["compliance"] * 100)
                
                    outputPath = os.path.join(roleToSave, f"{weekNumber}.csv")
                
                    dfWeek.to_csv(outputPath,index=False,encoding="utf-16")

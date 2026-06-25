import os
import csv
import pandas as pd

from sklearn.ensemble import VotingClassifier
from sklearn.tree import DecisionTreeClassifier


def CreateCSV(filePath, fieldnames):
    with open(filePath, mode="w", encoding="utf-16", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)


def UpdateCSV(csvPath, write):
    with open(csvPath, mode="a", encoding="utf-16", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(write)


source = "D:/RandomForest/"
directoryToSave = "D:/VotingClassifier/"

features = ["matches", "scoreMin", "scoreMax", "delta"]
target = "classifier"

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

                    dfAll = []
                    weeksUsed = []

                    weeks = sorted(os.listdir(taskPath))

                    for week in weeks:
                        weekPath = os.path.join(taskPath, week)

                        dfWeek = pd.read_csv(weekPath, encoding="utf-16")

                        dfAll.append(dfWeek)
                        weeksUsed.append(week)

                        dfTrain = pd.concat(dfAll, ignore_index=True)

                        X = dfTrain[features]
                        y = dfTrain[target]

                        clf = DecisionTreeClassifier()

                        model = VotingClassifier(estimators=[("dt", clf)],voting="hard")

                        model.fit(X, y)

                        print(f"[VOTING] Task: {task} | "f"Week predicted: {week} | "f"Weeks for training: {weeksUsed}")

                        dfWeek["ensemble"] = model.predict(dfWeek[features])

                        savePath = os.path.join(taskToSave, week)
                        dfWeek.to_csv(savePath, encoding="utf-16", index=False)

                
                                            
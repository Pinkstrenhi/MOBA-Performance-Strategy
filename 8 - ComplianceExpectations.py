import os
import pandas as pd

source = "D:/VotingClassifier/"
directoryToSave = "D:/ComplianceScores/"
complianceExpectations = "D:/ComplianceExpectations/"

def ComplianceScore(commitment, expected):
    if commitment == expected:
        return 1.0
    elif commitment == "Average" and expected in ["High", "Low"]:
        return 0.5
    else:
        return 0.0


columnsToRemove = ["cluster", "label", "classifier"]

expectations = {}
for file in os.listdir(complianceExpectations):
    role = file.replace(".csv", "").lower()
    expectations[role] = pd.read_csv(os.path.join(complianceExpectations, file))


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

                roleKey = role.lower()
                roleExpectations = expectations[roleKey]

                for task in os.listdir(rolePath):
                    taskPath = os.path.join(rolePath, task)
                    taskToSave = os.path.join(roleToSave, task)
                    os.makedirs(taskToSave, exist_ok=True)

                    expectedCommitment = roleExpectations[roleExpectations["Task"] == task]

                    if expectedCommitment.empty:
                        continue

                    expectedLabel = expectedCommitment["Compliance"].values[0]

                    for weekFile in os.listdir(taskPath):
                        weekPath = os.path.join(taskPath, weekFile)

                        df = pd.read_csv(weekPath, encoding="utf-16")
                        
                        if "ensemble" in df.columns:
                            df = df.rename(columns={"ensemble": "commitment"})

                        df["expected"] = expectedLabel
                        df["compliancescore"] = df["commitment"].apply(lambda x: ComplianceScore(x, expectedLabel))
                        
                        df = df.drop(columns=[c for c in columnsToRemove if c in df.columns])

                        savePath = os.path.join(taskToSave, weekFile)
                        df.to_csv(savePath, index=False, encoding="utf-8")

                    
                    
                    
import os
import pandas as pd

sourceScores = "D:/ComplianceScores/"
sourceTasks = "D:/RelevantTasks/"
directoryToSave = "D:/GameplaySuggestions/"

bestCriterion = "gini"
bestDepth = "20"
bestSplit = "10"

for year in os.listdir(sourceScores):
    yearPath = os.path.join(sourceScores, year)

    for league in os.listdir(yearPath):
        leaguePath = os.path.join(yearPath, league)

        for split in os.listdir(leaguePath):
            splitPath = os.path.join(leaguePath, split)

            relevantTasksPath = os.path.join(
                sourceTasks,
                f"RF_{league}_{split}_{bestCriterion}_depth{bestDepth}_split{bestSplit}.csv"
            )

            relevantTasks = pd.read_csv(relevantTasksPath)

            for role in os.listdir(splitPath):
                rolePath = os.path.join(splitPath, role)

                for task in os.listdir(rolePath):

                    taskRow = relevantTasks[relevantTasks["feature"] == task]

                    if taskRow.empty:
                        continue

                    contribution = taskRow["contributionNormalized"].values[0]

                    taskPath = os.path.join(rolePath, task)

                    for weekFile in os.listdir(taskPath):
                        weekFilePath = os.path.join(taskPath, weekFile)
                        
                        weekName = weekFile.split("_")[1]

                        df = pd.read_csv(weekFilePath)

                        df["meanScore"] = (df["scoreMin"] + df["scoreMax"]) / 2

                        totalMean = df["meanScore"].sum()
                        
                        if totalMean != 0:
                            df["normalizedScore"] = (df["meanScore"] / totalMean * 100).round(2)
                        else:
                            df["normalizedScore"] = 0

                        results = []

                        for row in df.itertuples():

                            player = row.playername
                            team = row.teamname
                            compliance = row.compliancescore

                            normalizedScore = row.normalizedScore

                            difference = contribution - normalizedScore

                            complianceSuggestion = ""

                            if compliance < 1:

                                increase = 1 - compliance

                                complianceSuggestion = (
                                    f"{player} should increase the Compliance score "
                                    f"({compliance:.2f}) on task {task} by {increase:.2f}"
                                )
                            else: 
                                complianceSuggestion = (
                                    f"{player} achieved max Compliance score"
                                )

                            differenceSuggestion = (
                                f"{task}: The difference between normalized "
                                f"({normalizedScore:.2f}%) score and contribution "
                                f"({contribution:.2f}%) is {difference:.2f}%"
                            )

                            results.append({
                                "player": player,
                                "team": team,
                                "role": role,
                                "task": task,
                                "complianceSuggestion": complianceSuggestion,
                                "differenceSuggestion": differenceSuggestion
                            })

                        savePath = os.path.join(
                            directoryToSave,
                            year,
                            league,
                            split,
                            role,
                            task
                        )

                        os.makedirs(savePath, exist_ok=True)

                        dfResults = pd.DataFrame(results)

                        dfResults.to_csv(
                            os.path.join(savePath, weekFile),
                            index=False
                        )



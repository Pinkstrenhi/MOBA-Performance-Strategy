import os
import pandas as pd
import matplotlib.pyplot as plt

source = "D:/VotingClassifier/"
directoryToSave = "D:/CommitmentEvolution/"

commitmentMap = {"Low": 0, "Average": 1, "High": 2}

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

                    dfs = []

                    for weekFile in os.listdir(taskPath):
                        weekPath = os.path.join(taskPath, weekFile)

                        weekNumber = int(weekFile.split(".")[0].split("_")[1])

                        df = pd.read_csv(weekPath, encoding="utf-16")
                        df["week"] = weekNumber

                        dfs.append(df)

                    if not dfs:
                        continue

                    dfAll = pd.concat(dfs, ignore_index=True)

                    dfAll = dfAll[["playername", "teamname", "week", "ensemble"]]

                    dfAll["commitmentNum"] = dfAll["ensemble"].map(commitmentMap)

                    for (player, team), dfPlayer in dfAll.groupby(["playername", "teamname"]):

                        dfPlayer = dfPlayer.sort_values("week")

                        plt.figure(figsize=(10, 5))
                        plt.plot(dfPlayer["week"],dfPlayer["commitmentNum"],marker="o")

                        plt.yticks([0, 1, 2], ["Low", "Average", "High"])
                        plt.xticks(dfPlayer["week"])
                        plt.xlabel("Week")
                        plt.ylabel("Commitment")
                        plt.title(f"Evolution of Commitment for '{player} ({team})' in Task '{task}' as a '{role}'")
                        plt.grid(True, axis="y", linestyle="--", alpha=0.6)
                        plt.tight_layout()

                        outputPath = os.path.join(taskToSave,f"{player}_{team}_week_{weekNumber}.png")
                        plt.savefig(outputPath)
                        plt.close()

                    
                    
                    
                    
                    
                    
                    
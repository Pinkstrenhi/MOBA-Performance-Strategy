import os
import pandas as pd 

source = "D:/OutcomePredictionRF/Contribution/"
directoryToSave = "D:/RelevantTasks/"

os.makedirs(directoryToSave, exist_ok=True)

bestCriterion = "gini"
bestDepth = "20"
bestSplit = "10"

for leagueSplit in os.listdir(source):
    leagueSplitPath = os.path.join(source, leagueSplit)
    
    for file in os.listdir(leagueSplitPath):
        
        fileCheck = f"RF_{leagueSplit}_{bestCriterion}_depth{bestDepth}_split{bestSplit}.csv"
        
        if file == fileCheck:

            filePath = os.path.join(leagueSplitPath, file)

            df = pd.read_csv(filePath)
            
            df["contributionNormalized"] = (
                df["contribution"] / df["contribution"].sum() * 100
            ).round(2)

            meanContribution = round(df["contributionNormalized"].mean(), 2)
            
            print(meanContribution)

            relevantTasks = df[df["contributionNormalized"] > meanContribution]

            savePath = os.path.join(directoryToSave, fileCheck)

            relevantTasks.to_csv(savePath, index=False)

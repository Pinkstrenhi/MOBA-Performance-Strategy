import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedKFold

def FolderPath(directory, pathName):
    path = os.path.join(directory, pathName)
    if not os.path.exists(path):
        os.mkdir(path)
    return path

source = "D:/VectorToPredictOutcomeAsNumbers/"
directoryToSave = "D:/OutcomePredictionRF/"

directoryPrediction = FolderPath(directoryToSave,"Predictions")
directoryResults = FolderPath(directoryToSave,"Results")
directoryContribution = FolderPath(directoryToSave,"Contribution")

strings = ["playername", "teamname", "role", "week"]

stratifiedKFold = StratifiedKFold(shuffle=True, random_state=42)

rfParameters = {
                   "criterion": "gini",
                   "max_depth": 20,
                   "min_samples_split": 10
               }

allResults = []

for league in os.listdir(source):
    leaguePath = os.path.join(source, league)
    
    for year in os.listdir(leaguePath):
        yearPath = os.path.join(leaguePath, year)
        
        for split in os.listdir(yearPath):
            splitPath = os.path.join(yearPath, split)
            
            predictionPath = FolderPath(directoryPrediction, f"{league}_{year}_{split}")
            contributionPath = FolderPath(directoryContribution, f"{league}_{year}_{split}")        
            
            for file in os.listdir(splitPath):
                filePath = os.path.join(splitPath, file)
            
                df = pd.read_csv(filePath, encoding="utf-16")
                
                X = df.drop(strings + ["result"], axis=1)
                y = df["result"]
                
                X = X.apply(pd.to_numeric, errors="coerce")
                X = X.replace([np.inf, -np.inf], np.nan)
                X = X.fillna(0)
                
                model = RandomForestClassifier(**rfParameters)
                
                accuracies = []
                
                for trainIndex, testIndex in stratifiedKFold.split(X, y):
                    trainX, testX = X.iloc[trainIndex], X.iloc[testIndex]
                    trainY, testY = y.iloc[trainIndex], y.iloc[testIndex]
                    
                    model.fit(trainX, trainY)
                    prediction = model.predict(testX)
                    accuracyScore = accuracy_score(testY, prediction)
                    accuracies.append(accuracyScore)
                
                meanAccuracy = round((sum(accuracies) / len(accuracies)) * 100, 2)
                
                model.fit(X, y)
                predictionY = model.predict(X)
                
                dfPrediction = pd.DataFrame({
                    "predicted": predictionY,
                    "actual": y.values
                })
                
                fileToSave = os.path.join(predictionPath, f"RF_{file}")
                dfPrediction.to_csv(fileToSave, index=False)
      
                allResults.append({
                    "league": league,
                    "year": year,
                    "split": split,
                    "classifier": "RandomForest",
                    "parameters": str(rfParameters),
                    "meanAccuracy": meanAccuracy
                })
                
                try:
                    contribution = model.feature_importances_
                    
                    dfContribution = pd.DataFrame({
                        "feature": X.columns,
                        "contribution": contribution
                    })
                    
                    dfContribution = dfContribution.sort_values(
                        by="contribution",
                        ascending=False
                    )
                    
                    contributionFile = os.path.join(contributionPath, f"RF_{file}")
                    dfContribution.to_csv(contributionFile, index=False)
                except:
                    continue
                
dfFinalResults = pd.DataFrame(allResults)

finalResultsPath = os.path.join(directoryResults, "results.csv")

dfFinalResults.to_csv(finalResultsPath, index=False, sep=";")
import os
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedKFold

def FolderPath(directory, pathName):
    path = os.path.join(directory, pathName)
    if not os.path.exists(path):
        os.mkdir(path)
    return path

source = "D:/VectorToPredictOutcomeAsNumbers/"
directoryToSave = "D:/OutcomePredictionLGBM/"

directoryPrediction = FolderPath(directoryToSave,"Predictions")
directoryResults = FolderPath(directoryToSave,"Results")
directoryContribution = FolderPath(directoryToSave,"Contribution")

strings = ["playername", "teamname", "role", "week"]

stratifiedKFold = StratifiedKFold(shuffle=True, random_state=42)

lgbmParameters = {
                    "num_leaves": 31,
                    "learning_rate": 0.1,
                    "n_estimators": 50,
                    "random_state": 42
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
            
                df = pd.read_csv(filePath, encoding = "utf-16")
                
                X = df.drop(strings + ["result"], axis=1)
                y = df["result"]
                
                model = LGBMClassifier(**lgbmParameters)
                
                accuracies = []
                
                for trainIndex, testIndex in stratifiedKFold.split(X, y):
                    trainX, testX = X.iloc[trainIndex], X.iloc[testIndex]
                    trainY, testY = y[trainIndex], y[testIndex]
                    
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
                
                fileToSave = os.path.join(predictionPath, f"LGBM_{file}")
                dfPrediction.to_csv(fileToSave, index=False)
      
                dfLog = pd.DataFrame({
                                        "classifier": ["LGBM"],
                                        "parameters": [str(lgbmParameters)],
                                        "meanAccuracy": [meanAccuracy]                                    
                                    })
                                
                allResults.append({
                                    "league": league,
                                    "year": year,
                                    "split": split,
                                    "classifier": "LGBM",
                                    "parameters": str(lgbmParameters),
                                    "meanAccuracy": meanAccuracy
                                 })
                
                try:
                    contribution = model.feature_importances_
                    
                    dfContribution = pd.DataFrame({"feature": X.columns,"contribution": contribution})
                    
                    dfContribution = dfContribution.sort_values(by="contribution",ascending=False)
                    
                    contributionFile = os.path.join(contributionPath, f"LGBM_{file}")
                    dfContribution.to_csv(contributionFile, index=False)
                except:
                    continue
                
dfFinalResults = pd.DataFrame(allResults)

finalResultsPath = os.path.join(directoryResults, "results.csv")

dfFinalResults.to_csv(finalResultsPath, index=False, sep=";")
import os
import numpy as np
import pandas as pd
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from lightgbm import LGBMClassifier

def FolderPath(directory, pathName):
    path = os.path.join(directory, pathName)
    if not os.path.exists(path):
        os.mkdir(path)
    return path

source = "D:/VectorToPredictOutcomeAsNumbers/"
directoryToSave = "D:/OutcomePrediction/"

directoryPrediction = FolderPath(directoryToSave,"Predictions")
directoryResults = FolderPath(directoryToSave,"Results")
directoryContribution = FolderPath(directoryToSave,"Contribution")

strings = ["playername", "teamname", "role", "week"]

stratifiedKFold = StratifiedKFold(shuffle=True, random_state=42)
 
allClassifiers = {
    "DT": {
        "classifier": DecisionTreeClassifier,
        "parameters": {
            "criterion": ["gini", "entropy", "log_loss"],
            "splitter": ["best", "random"],
            "max_depth": [None, 5, 10, 15],
            "random_state": [42]
        }
    },
    "RF": {
        "classifier": RandomForestClassifier,
        "parameters": {
            "criterion": ["gini", "entropy", "log_loss"],
            "max_depth": [None, 5, 10, 15, 20, 30],
            "min_samples_split": [2, 5, 10, 15]
        }
    },
    "LGBM": {
        "classifier": LGBMClassifier,
        "parameters": {
            "num_leaves": [31, 50],
            "learning_rate": [0.01, 0.1],
            "n_estimators": [50, 100, 200],
            "random_state": [42]
        }
    },
    "MLP": {
        "classifier": MLPClassifier,
        "parameters": {
            "hidden_layer_sizes": [(50,), (100,), (50, 50)],
            "activation": ["identity", "logistic", "tanh", "relu"],
            "solver": ["lbfgs", "sgd", "adam"],
            "learning_rate": ["constant", "invscaling", "adaptive"]
        }
    }
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

                for classifierName, modelData in allClassifiers.items():

                    classifier = modelData["classifier"]
                    parameters = modelData["parameters"]

                    print("-" * 60)
                    print(f"{league} | {year} | {split} | {file}")
                    print(f"Running {classifierName}")

                    gridSearch = GridSearchCV(
                        classifier(),
                        parameters,
                        cv=stratifiedKFold,
                        scoring="accuracy"
                    )

                    gridSearch.fit(X, y)

                    bestModel = gridSearch.best_estimator_
                    bestParameters = gridSearch.best_params_
                    bestScore = gridSearch.best_score_

                    print(f"Best model: {bestModel}")
                    print(f"Best parameters: {bestParameters}")
                    print(f"Best accuracy (GridSearch): {bestScore}")

                    predictionY = bestModel.predict(X)

                 
                    dfPrediction = pd.DataFrame({
                        "predicted": predictionY,
                        "actual": y
                    })

                    fileToSave = os.path.join(
                        predictionPath,
                        f"{classifierName}_{file}"
                    )

                    dfPrediction.to_csv(fileToSave, index=False)

                    allResults.append({
                        "league": league,
                        "year": year,
                        "split": split,
                        "file": file,
                        "classifier": classifierName,
                        "parameters": str(bestParameters),
                        "meanAccuracy": bestScore
                    })

                    try:
                        contribution = bestModel.feature_importances_

                        dfContribution = pd.DataFrame({
                            "feature": X.columns,
                            "contribution": contribution
                        })

                        dfContribution = dfContribution.sort_values(
                            by="contribution",
                            ascending=False
                        )

                        contributionFile = os.path.join(
                            contributionPath,
                            f"{classifierName}_{file}"
                        )

                        dfContribution.to_csv(contributionFile, index=False)

                    except:
                        pass


dfFinalResults = pd.DataFrame(allResults)
finalResultsPath = os.path.join(directoryResults, "results.csv")
dfFinalResults.to_csv(finalResultsPath, index=False, sep=";")
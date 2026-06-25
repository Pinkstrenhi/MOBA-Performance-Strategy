import os
import csv
import pandas as pd
from sklearn.cluster import KMeans

def CreateCSV(filePath,fieldnames):
    with open(filePath, mode="w",encoding="utf-16", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)
def UpdateCSV(csvPath,write):
    with open(csvPath, mode="a",encoding="utf-16", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(write)
def ClusterKmeans(df):
    k = 3
    kmeans = KMeans(n_clusters = k)
    kmeans.fit(df)
    df["cluster"] = kmeans.labels_
    return df


source = "D:/CommitmentVectors/"
directoryToSave = "D:/Cluster/"

columnsID = ["playername","teamname","result"]

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
                    
                    for week in os.listdir(taskPath):
                        weekPath = os.path.join(taskPath, week)
                        
                        
                        df = pd.read_csv(weekPath, encoding = "utf-16")
                        
                        dfId = df[columnsID]

                        columnsCluster = []
                        for column in df.columns:
                            if column in columnsID or df[column].dtype == object:
                                columnsCluster.append(column)

                        dfCluster = df.drop(columns=columnsCluster)

                        dfCluster = ClusterKmeans(dfCluster)

                        dfFinal = pd.concat([dfId, dfCluster], axis=1)

                        csvPath = os.path.join(taskToSave, week)

                        CreateCSV(csvPath, dfFinal.columns)

                        for _, row in dfFinal.iterrows():
                            UpdateCSV(csvPath, row)
                
                
                
                
                
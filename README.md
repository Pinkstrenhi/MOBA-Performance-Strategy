# MOBA Player Engagement and Performance Analysis Pipeline

This repository contains a 16-step pipeline designed to analyze player engagement in MOBA games (specifically tested with *League of Legends* match data). The method evaluates how players perform role-related tasks, measures their alignment with team expectations, predicts match outcomes, and generates gameplay improvement suggestions.

---

## Overview of the Pipeline

### **1. CommitmentVectors.py**

Prepares and structures the raw data for all subsequent steps.

### **2. Cluster.py**

Applies the K-Means algorithm to group the data into **3 clusters**.

### **3. ClusterCleanScore.py**

Removes samples that do not result in exactly **3 clusters**, which is required for the next steps.

### **4. ClusterLabel.py**

Assigns labels (**Low**, **Average**, **High**) to clusters based on the mean value of `scoreMax`.

---

### **5. RandomForest.py**

Trains Random Forest classifiers to identify player behavior patterns for each analyzed period.

### **6. VotingClassifier.py**

Combines multiple Random Forest classifiers using a Voting Classifier to determine final **Commitment levels**, considering historical predictions.

### **7. CommitmentEvolution.py**

Generates visualizations showing how player Commitment evolves over time.

---

### **8. ComplianceExpectations.py**

Calculates **Compliance scores** by comparing player Commitment levels with expected behavior for each role.
Possible scores: **0**, **0.5**, or **1**.

### **9. CompliancePercent.py**

Computes the overall compliance percentage by dividing the total sum of all scores by the number of analyzed tasks.

---

### **10. VectorToPredictOutcome.py**

Combines Commitment levels and Compliance scores into a dataset used for outcome prediction.

### **11. VectorToPredictOutcomeAsNumbers.py**

Converts categorical Commitment levels into numeric values:

* Low → 1
* Average → 2
* High → 3

This ensures compatibility with prediction models.

---

### **12. OutcomePredictionGSCV.py**

Uses GridSearchCV to identify the best models and hyperparameters for predicting match outcomes.

### **13. OutcomePredictionLGBM.py**

Performs an exhaustive parameter search for the LightGBM model.

### **14. OutcomePredictionRF.py**

Performs an exhaustive parameter search for the Random Forest model.

---

### **15. RelevantTasks.py**

Identifies the most important tasks for match outcomes.
A task is considered relevant if its contribution is **greater than or equal to the average contribution**.

### **16. GameplaySuggestions.py**

Generates gameplay improvement suggestions of relevant tasks based on:

* Compliance scores
* Differences between normalized performance metrics

---

## Final Output

By the end of the pipeline, the system provides:

* Player Commitment analysis over time
* Alignment with expected role behavior (Compliance)
* Match outcome predictions
* Actionable gameplay suggestions for performance improvement

---

## Notes

* The pipeline assumes that clustering always results in **exactly 3 groups**.
* Designed and validated using *League of Legends* data, but adaptable to other MOBA games.

---
 

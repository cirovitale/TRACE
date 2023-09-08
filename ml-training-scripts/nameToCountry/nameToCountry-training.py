import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, matthews_corrcoef, precision_score
from joblib import dump

# Undersample dataset
def undersampleDataset(dataset, column, targetCount):
    return dataset.groupby(column).apply(lambda x: x.sample(min(len(x), targetCount))).reset_index(drop=True)

# Load and clean dataset
def loadAndCleanDataset(filepath):
    dataset = pd.read_csv(filepath)
    datasetCleaned = dataset.dropna().copy()
    datasetCleaned['Name'] = datasetCleaned['Name'].str.lower()
    # Undersampling
    averageCount = int(datasetCleaned['Country'].value_counts().mean())
    datasetBalanced = undersampleDataset(datasetCleaned, 'Country', averageCount)
    return datasetBalanced

# Vectorize data
def vectorizeData(data, ngramRange=(1, 2)):
    vectorizer = TfidfVectorizer(ngram_range=ngramRange)
    X = vectorizer.fit_transform(data)
    return X, vectorizer

# Train model
def trainRandomForest(X_train, y_train, nEstimators=200, cv=3):
    model = RandomForestClassifier(n_estimators=nEstimators)
    scores = cross_val_score(model, X_train, y_train, cv=cv)
    model.fit(X_train, y_train)
    return model, scores

# Evaluate model
def evaluateModel(model, X_test, y_test):
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    mcc = matthews_corrcoef(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    return accuracy, mcc, precision

def main():
    dataset = loadAndCleanDataset("name_country.csv")
    X, vectorizer = vectorizeData(dataset['Name'])
    y = dataset['Country']
    # Split dataset in training and test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model, scores = trainRandomForest(X_train, y_train)
    print(f"Cross-validation scores: {scores}")
    print(f"Mean Cross-Validation Scores: {np.mean(scores)}")
    accuracy, mcc, precision = evaluateModel(model, X_test, y_test)
    print(f"ACCURACY {accuracy}")
    print(f"MCC {mcc}")
    print(f"Precision {precision}")
    dump(model, 'random_forest_model15.joblib')
    dump(vectorizer, 'tfidf_vectorizer15.joblib')

if __name__ == "__main__":
    main()
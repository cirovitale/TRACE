import joblib

# Load model and vectorizer
random_forest_model = joblib.load('./models/random_forest_model.joblib')
tfidf_vectorizer = joblib.load('./vectorizers/tfidf_vectorizer.joblib')

def predictFromName(name):
    if name is None or name == "":
        return None
    else:
        print('Prediction from name of ', name + '...')

    if not isinstance(name, str) or not name:
        print(f"[NAME PREDICT] Name format not valid")
        return {"error":"Name format not valid", "status": 400 }
    
    try:
        vectorizedName = tfidf_vectorizer.transform([name])
    except Exception as e:
        print(f"[NAME PREDICT] Error during name vectorization: {str(e)}")
        return {"error":f"Error during vectorization: {str(e)}", "status": 500 }
    
    try:
        result = random_forest_model.predict(vectorizedName)
        return result[0]
    except Exception as e:
        print(f"[NAME PREDICT] Error during ML prediction: {str(e)}")
        return {"error":f"Error during prediction: {str(e)}", "status": 500 }

import joblib

# Load model and vectorizer
random_forest_model = joblib.load('./models/random_forest_model.joblib')
tfidf_vectorizer = joblib.load('./vectorizers/tfidf_vectorizer.joblib')

THRESHOLD = 0.5

def containNums(name):
    return any(char.isdigit() for char in name)

def predictFromName(name):
    if name is None or name == "" or containNums(name):
        return None
    else:
        print('Prediction from name of ', name + '...')

    if not isinstance(name, str) or not name:
        print(f"[NAME PREDICT] Name format not valid")
        return {"error":"Name format not valid", "status": 400 }
    
    try:
        # 2. Vectorize the input
        vectorizedName = tfidf_vectorizer.transform([name])
    except Exception as e:
        print(f"[NAME PREDICT] Error during name vectorization: {str(e)}")
        return {"error":f"Error during vectorization: {str(e)}", "status": 500 }
    
    try:
        # 3. Predict using the model
        prediction = random_forest_model.predict(vectorizedName)
        predictionProba = random_forest_model.predict_proba(vectorizedName)
        
        classIndex = list(random_forest_model.classes_).index(prediction[0])
        
        if predictionProba[0][classIndex] < THRESHOLD:
            return None
        
        return prediction[0]
    
    except Exception as e:
        print(f"[NAME PREDICT] Error during ML prediction: {str(e)}")
        return {"error":f"Error during prediction: {str(e)}", "status": 500 }

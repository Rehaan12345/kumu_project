import firebase_admin
from firebase_admin import credentials, storage, firestore

cred = credentials.Certificate("credentials.json")
fire_app = firebase_admin.initialize_app(cred)

firebaseConfig = {
  "apiKey": "AIzaSyBj3HivDta8E8HN0FYQJetBx7JCffS2pGE",
  "authDomain": "kumuweb-dae5e.firebaseapp.com",
  "projectId": "kumuweb-dae5e",
  "storageBucket": "kumuweb-dae5e.appspot.com",
  "messagingSenderId": "42512105158",
  "appId": "1:42512105158:web:7c013eb6de9583c20e21c7",
  "measurementId": "G-PL6D41DH8K"
}

db = firestore.client()

def update_sheet(collection, vals):
    try:
        for val in vals:
            result = db.collection(collection).document(val).set(
                {
                    "From": vals[0],
                    "To": val
                }
            )
        return {"status": f"Success: {result}"}
    except Exception as e:
        return {"status": f"Failure: {e}"}
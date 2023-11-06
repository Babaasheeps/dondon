# Firestore configuration file
# Initializes firebase

import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# TODO: Change to os path
# Use a service account.
service_account_path = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
cred = credentials.Certificate(service_account_path)

# Initialize firebase
app = firebase_admin.initialize_app()

# Connect to database
db = firestore.client()

# if __name__ == "__main__":
#      service_account_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
#      if service_account_path:
#          print(f"Service account path: {service_account_path}")
#      else:
#          print("GOOGLE_APPLICATION_CREDENTIALS environment variable is not set.")
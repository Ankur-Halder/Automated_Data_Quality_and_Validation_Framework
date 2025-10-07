import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
import logging 
 
def prep_data(data):
    total_rows, _ = data.shape
    X = pd.DataFrame(data)
    num_col = X.select_dtypes(include=['int', 'float']).columns.tolist()
    obj_col = X.select_dtypes(include=['object']).columns.tolist()

    # Encode categorical
    for col in obj_col:
        if X[col].isnull().any():
            X[col] = X[col].fillna(X[col].mode()[0])
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])

    # Scale numerical
    for col in num_col:
        if X[col].isnull().any():
            X[col] = X[col].fillna(X[col].mean())
        scaler = StandardScaler()
        X[col] = scaler.fit_transform(X[[col]])
    try:
        logging.info("Dataset Processed")
        return X
    except Exception as e:
        logging.error(f"Couldn't Process dataset:{e}")
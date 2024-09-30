# -*- coding: utf-8 -*-
"""app2.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1xKAMhXsoJ2dPlPz_Qxa3ZLILQ4apfQMF
"""

# loan_eligibility_predictor.py

import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt

# Title of the web app
st.title("AI-Powered Loan Eligibility Predictor")

# Description
st.write("""
This application helps financial institutions predict loan eligibility of applicants based on various input features such as income, loan amount, credit score, and more. The application is powered by machine learning.
""")

# Hardcoded dataset for training
@st.cache_data
def load_data():
    # Simple dataset for loan eligibility
    data = {
        'ApplicantIncome': [5000, 6000, 7000, 8000, 9000, 3000, 4000, 6500, 12000, 15000],
        'CoapplicantIncome': [0, 1500, 0, 2000, 3000, 0, 0, 1800, 0, 4000],
        'LoanAmount': [150, 200, 250, 300, 350, 100, 120, 275, 400, 500],
        'Loan_Amount_Term': [12, 24, 36, 48, 60, 12, 24, 36, 48, 60],
        'Credit_History': [1, 0, 1, 1, 0, 1, 1, 0, 1, 1],
        'Property_Area_Semiurban': [0, 1, 0, 0, 1, 1, 0, 1, 0, 0],
        'Property_Area_Urban': [1, 0, 1, 0, 0, 0, 1, 0, 1, 1],
        'Eligible': [1, 0, 1, 1, 0, 1, 1, 0, 1, 1]
    }
    df = pd.DataFrame(data)
    return df

df = load_data()

# Display dataset overview
st.write("### Dataset Overview")
st.write(df)

# Preprocessing: Define features (X) and target (y)
X = df.drop('Eligible', axis=1)
y = df['Eligible']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the RandomForest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Model performance
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
st.write("### Model Accuracy:", accuracy)

# Model evaluation
st.write("#### Classification Report")
st.text(classification_report(y_test, y_pred))

# Plot confusion matrix
st.write("#### Confusion Matrix")
conf_matrix = confusion_matrix(y_test, y_pred)
st.write(conf_matrix)

# User input section for predictions
st.write("### Make a Prediction")
st.write("Enter the details to check if you're eligible for a loan:")

# User input fields
applicant_income = st.number_input("Applicant Income", min_value=0, max_value=100000, value=5000)
coapplicant_income = st.number_input("Coapplicant Income", min_value=0, max_value=50000, value=0)
loan_amount = st.number_input("Loan Amount", min_value=0, max_value=1000, value=150)
loan_term = st.number_input("Loan Term (in months)", min_value=1, max_value=360, value=12)
credit_history = st.selectbox("Credit History (1 = Good, 0 = Bad)", (1, 0))
property_area = st.selectbox("Property Area", ('Urban', 'Semiurban', 'Rural'))

# Convert user inputs to match the model features
property_area_map = {'Urban': [1, 0], 'Semiurban': [0, 1], 'Rural': [0, 0]}
property_area_features = property_area_map[property_area]

# Create a button for prediction
if st.button("Predict Loan Eligibility"):
    # Arrange the input data
    input_data = pd.DataFrame({
        'ApplicantIncome': [applicant_income],
        'CoapplicantIncome': [coapplicant_income],
        'LoanAmount': [loan_amount],
        'Loan_Amount_Term': [loan_term],
        'Credit_History': [credit_history],
        'Property_Area_Semiurban': [property_area_features[0]],
        'Property_Area_Urban': [property_area_features[1]]
    })

    # Scale the input data
    input_data_scaled = scaler.transform(input_data)

    # Make predictions
    prediction = model.predict(input_data_scaled)

    # Output the prediction result
    if prediction[0] == 1:
        st.success("The model predicts that the applicant is eligible for the loan.")
    else:
        st.error("The model predicts that the applicant is NOT eligible for the loan.")


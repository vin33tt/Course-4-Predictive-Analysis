# -*- coding: utf-8 -*-
"""LVADSUSR132FINAL-ML-LAB1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18rjzGlfWKyEuEArrFke8WgimwjerO8Yi
"""

import pandas as pd
import numpy as np
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier

df=pd.read_csv('/content/loan_approval.csv')
loan_data=df
df.head()

df.info()
df.isnull().sum()

numerical_summary = df.describe()
numerical_summary

loan_data.columns = loan_data.columns.str.strip()
missing_values_corrected = loan_data.isnull().sum()
missing_values_corrected

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
print("Shape of the DataFrame:", df.shape)
print("Descriptive Statistics:")
print(df.describe())
print("\nInfo:")
print(df.info())
print("\nFirst few rows:")
print(df.head())
print("\nLast few rows:")
print(df.tail())
print("\nUnique values and counts for categorical columns:")
for column in df.select_dtypes(include=['object']):
    print(column + ":")
    print(df[column].value_counts())
    print()
print("\nCorrelation Matrix:")
print(df.corr())
df.hist(figsize=(10, 8))
plt.tight_layout()
plt.show()
for column in df.select_dtypes(include=['object']):
    plt.figure(figsize=(8, 6))
    sns.countplot(data=df, x=column)
    plt.title("Count of " + column)
    plt.xticks(rotation=45)
    plt.show()

target_distribution_corrected = loan_data['loan_status'].value_counts(normalize=True)
target_distribution_corrected
def remove_outliers(df, features):
    outlier_indices = []

    for feature in features:
        Q1 = np.percentile(df[feature], 25)
        Q3 = np.percentile(df[feature], 75)
        IQR = Q3 - Q1
        outlier_step = 1.5 * IQR
        feature_outlier_indices = df[(df[feature] < Q1 - outlier_step) | (df[feature] > Q3 + outlier_step)].index
        outlier_indices.extend(feature_outlier_indices)

    outlier_indices = [index for index, count in Counter(outlier_indices).items() if count > 2]
    df_cleaned = df.drop(outlier_indices)
    return df_cleaned

num_features=['no_of_dependents', 'income_annum', 'loan_amount', 'loan_term', 'cibil_score',
              'residential_assets_value', 'commercial_assets_value', 'luxury_assets_value', 'bank_asset_value']
loan_data_cleaned = remove_outliers(loan_data, num_features )
loan_data_cleaned.info()

categorical_features = ['education', 'self_employed']
preprocessor = ColumnTransformer(transformers=[
    ('num', StandardScaler(), num_features),
    ('cat', OneHotEncoder(), categorical_features)
])
X = loan_data_cleaned.drop('loan_status', axis=1)
y = loan_data_cleaned['loan_status']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Decision Tree": DecisionTreeClassifier(),
    "Random Forest": RandomForestClassifier(),
    "Gradient Boosting": GradientBoostingClassifier()
}
results = {}
for name, model in models.items():
    pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('model', model)])
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)
    results[name] = {"Accuracy": accuracy, "Confusion Matrix": conf_matrix}
for model_name, metrics in results.items():
    print(f"{model_name}: Accuracy = {metrics['Accuracy']:.2f}, Confusion Matrix = {metrics['Confusion Matrix']}")
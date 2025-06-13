import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Load dataset
df = pd.read_csv(r"uploaded_data/generated_data_v3_1.csv")

# Preprocessing function
def preprocess_data(df):
    df['Validated_Semesters'] = df[[f'S{i}' for i in range(1, 13)]].apply(
        lambda x: sum(1 for s in x if s == 'validate'), axis=1)
    df['Repeated_Semesters'] = df[[f'S{i}' for i in range(1, 13)]].apply(
        lambda x: sum(1 for s in x if s == 'repeated'), axis=1)
    df['Failed_Semesters'] = df[[f'S{i}' for i in range(1, 13)]].apply(
        lambda x: sum(1 for s in x if s == 'no validate'), axis=1)

    features = ['Mark', 'Scholarship', 'Gender', 'School', 'Specialty',
                'Validated_Semesters', 'Repeated_Semesters', 'Failed_Semesters']
    X = df[features]
    y = df['Graduated']
    return X, y

X, y = preprocess_data(df)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

# Preprocessing and model pipeline
numeric_features = ['Mark', 'Validated_Semesters', 'Repeated_Semesters', 'Failed_Semesters']
categorical_features = ['Gender', 'School', 'Specialty']

numeric_transformer = Pipeline(steps=[
    ('scaler', StandardScaler())
])
categorical_transformer = Pipeline(steps=[
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(transformers=[
    ('num', numeric_transformer, numeric_features),
    ('cat', categorical_transformer, categorical_features)
])

model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', GradientBoostingClassifier(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=5,
        min_samples_split=20,
        min_samples_leaf=10,
        max_features='sqrt',
        subsample=0.8,
        random_state=42
    ))
])

# Train model
model.fit(X_train, y_train)

# Save model and test set for later evaluation
joblib.dump(model, 'model/student_gb_model.pkl')
joblib.dump((X_test, y_test), 'model/student_test_data.pkl')

print("Model and test data saved successfully.")

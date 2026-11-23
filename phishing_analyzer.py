"""
Phishing Email Analyzer - training
Built by Astha Patel

Trains a TF-IDF + Logistic Regression classifier on phishing_email.csv,
prints its test results, saves charts, and saves the model to models/
so detect.py can use it.

Run:  python3 phishing_analyzer.py
Needs phishing_email.csv in this folder (see README: "The Data").
"""

import os
import sys
import warnings

import joblib
import matplotlib
matplotlib.use("Agg")  # save charts without opening windows
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

warnings.filterwarnings("ignore")

DATA_PATH = "phishing_email.csv"
MODEL_DIR = "models"

print("=" * 50)
print("PHISHING EMAIL ANALYZER - TRAINING")
print("=" * 50)

# 1. Load the dataset
if not os.path.exists(DATA_PATH):
    sys.exit(f"\n{DATA_PATH} not found. Download it first (see README: 'The Data').")

df = pd.read_csv(DATA_PATH).dropna()
print(f"\nLoaded {len(df):,} emails "
      f"({int((df['label'] == 1).sum()):,} phishing, {int((df['label'] == 0).sum()):,} legitimate)")

# 2. Split 80% train / 20% test
X_train, X_test, y_train, y_test = train_test_split(
    df["text_combined"], df["label"], test_size=0.2, random_state=42
)

# 3. Turn text into TF-IDF features
print("\nConverting emails to TF-IDF features (about 30 seconds)...")
vectorizer = TfidfVectorizer(max_features=5000, stop_words="english")
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# 4. Train
print("Training Logistic Regression...")
model = LogisticRegression(max_iter=1000)
model.fit(X_train_tfidf, y_train)

# 5. Evaluate
y_pred = model.predict(X_test_tfidf)
print(f"\nTest accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")
print(classification_report(y_test, y_pred, target_names=["Legitimate", "Phishing"]))

# 6. Charts
plt.figure(figsize=(6, 4))
df["label"].value_counts().sort_index().plot(kind="bar", color=["#2ecc71", "#e74c3c"], edgecolor="black")
plt.title("Legitimate vs Phishing Emails", fontweight="bold")
plt.xticks([0, 1], ["Legitimate", "Phishing"], rotation=0)
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("email_distribution.png", dpi=150)
plt.close()

plt.figure(figsize=(6, 5))
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt="d", cmap="Blues",
            xticklabels=["Legitimate", "Phishing"], yticklabels=["Legitimate", "Phishing"])
plt.title("Confusion Matrix - Phishing Email Detector", fontweight="bold")
plt.ylabel("Actual")
plt.xlabel("Predicted")
plt.tight_layout()
plt.savefig("confusion_matrix.png", dpi=150)
plt.close()
print("Saved email_distribution.png and confusion_matrix.png")

# 7. Save the model for detect.py
os.makedirs(MODEL_DIR, exist_ok=True)
joblib.dump(vectorizer, os.path.join(MODEL_DIR, "vectorizer.pkl"))
joblib.dump(model, os.path.join(MODEL_DIR, "model.pkl"))
print("Saved models/vectorizer.pkl and models/model.pkl")
print("\nNext: python3 detect.py")

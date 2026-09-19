import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

def train():
    df = pd.read_csv("dataset.csv")
    model = make_pipeline(TfidfVectorizer(), MultinomialNB())
    model.fit(df["text"], df["label"])
    joblib.dump(model, "spam_model.joblib")

if __name__ == "__main__":
    train()
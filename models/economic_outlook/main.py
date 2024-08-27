import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, accuracy_score
import joblib
import nltk
from nltk.corpus import stopwords
import argparse
import re


nltk.download('stopwords')
stop_words = stopwords.words('english')


def sanitize_filename(name):
    return re.sub(r'[^\w\s-]', '', name).replace(' ', '_')


def main(train_file, model_output, test_file=None, test_output=None):
    df = pd.read_csv(train_file)
    df['postContent'] = df['postContent'].fillna('')
    df['is_economic_outlook'] = df['theme'].apply(lambda theme: 1 if theme == 'Economic Outlook' else 0)
    vectorizer = TfidfVectorizer(stop_words=stop_words, max_features=10000, ngram_range=(1,2))
    pipeline = Pipeline([
        ('tfidf', vectorizer),
        ('clf', LogisticRegression(solver='liblinear'))
    ])
    param_grid = {
        'tfidf__max_features': [5000, 10000, 20000],
        'tfidf__ngram_range': [(1,1,), (1,2)],
        'clf__C': [0.1, 1, 10]
    }
    
    if test_file:
        grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='accuracy')
        grid_search.fit(df['postContent'], df['is_economic_outlook'])
        print(f"Best parameters: {grid_search.best_params_}")
        print(f"Best cross-validation accuracy: {grid_search.best_score_}")
        best_model = grid_search.best_estimator_
        best_model.fit(df['postContent'], df['is_economic_outlook'])
        joblib.dump(best_model, model_output)
        print(f"Model trained and saved as {model_output}")
        df_test = pd.read_csv(test_file)
        df_test['postContent'] = df_test['postContent'].fillna('')
        if 'theme' in df_test.columns:
            df_test['is_economic_outlook'] = df_test['theme'].apply(lambda theme: 1 if theme == 'Economic Outlook' else 0)
        else:
            raise KeyError("The test file must contain a 'theme' column to create 'is_economic_outlook' labels for evaluation.")
        predictions = best_model.predict(df_test['postContent'])
        df_test['prediction'] = predictions
        print("Classification Report on the external test set:")
        print(classification_report(df_test['is_economic_outlook'], predictions))
        print("Accuracy on the external test set:", accuracy_score(df_test['is_economic_outlook'], predictions))
        df_test.to_csv(test_output, index=False)
        print(f"Predictions saved to {test_output}")
    else:
        X_train, X_test, y_train, y_test = train_test_split(df['postContent'], df['is_economic_outlook'], test_size=0.2, random_state=42)
        grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='accuracy')
        grid_search.fit(X_train, y_train)
        print(f"Best parameters: {grid_search.best_params_}")
        print(f"Best cross-validation accuracy: {grid_search.best_score_}")
        best_model = grid_search.best_estimator_
        best_model.fit(X_train, y_train)
        joblib.dump(best_model, model_output)
        print(f"Model trained and saved as {model_output}")
        y_pred = best_model.predict(X_test)
        print("Classification Report on the internal test set:")
        print(classification_report(y_test, y_pred))
        print("Accuracy on the internal test set:", accuracy_score(y_test, y_pred))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a binary classifier for 'Economic Outlook' theme.")
    parser.add_argument('train_file', type=str, help='Path to the training CSV file')
    parser.add_argument('model_output', type=str, help='Path to save the trained model')
    parser.add_argument('--test_file', type=str, help='Path to the external test CSV file', default=None)
    parser.add_argument('--test_output', type=str, help='Path to save the test predictions', default=None)

    args=parser.parse_args()
    main(args.train_file, args.model_output, args.test_file, args.test_output)

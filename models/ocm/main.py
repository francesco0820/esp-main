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

# Download NLTK stopwords
#nltk.download('stopwords')
#stop_words = stopwords.words('english')

# Download NLTK stopwords
nltk.download('stopwords')
 
# Load NLTK stopwords
nltk_stop_words = set(stopwords.words('english'))
 
# Load custom stopwords from file
with open('stopwords.txt', 'r') as file:
    custom_stop_words = set(line.strip() for line in file)
 
 # Combine NLTK stopwords with custom stopwords
stop_words = nltk_stop_words.union(custom_stop_words)
 
# Preprocess stopwords consistently with text preprocessing
#
def preprocess_stopwords(stopwords_set):
 
    processed_stopwords = set()
    for word in stopwords_set:
    # Apply the same preprocessing as your text data
            word = word.lower()  # Lowercase
            word = re.sub(r'\W+', '', word)  # Remove non-word characters
            processed_stopwords.add(word)
    return processed_stopwords
   
    # Apply preprocessing to the stopwords
stop_words = list(preprocess_stopwords(stop_words))


def sanitize_filename(name):
    return re.sub(r'[^\w\s-]', '', name).replace(' ', '_')


def main(train_file, model_output, test_file=None, test_output=None):
    # Load the preprocessed dataset
    df = pd.read_csv(train_file)

    # Handle NaN values in 'postContent'
    df['postContent'] = df['postContent'].fillna('')

    # Define binary labels based on the themes
    df['is_ocm'] = df['themes'].apply(lambda theme: 1 if theme == 'Organizational Change Management' else 0)

    # Vectorizer to transform the text data
    vectorizer = TfidfVectorizer(stop_words=stop_words, max_features=10000, ngram_range=(1, 2))

    # Build a pipeline with a classifier
    pipeline = Pipeline([
        ('tfidf', vectorizer),
        ('clf', LogisticRegression(solver='liblinear'))
    ])

    # Define hyperparameters to tune
    param_grid = {
        'tfidf__max_features': [5000, 10000, 20000],
        'tfidf__ngram_range': [(1, 1), (1, 2)],
        'clf__C': [0.1, 1, 10]
    }

    if test_file:
        # Use GridSearchCV to find the best hyperparameters on the entire training set
        grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='accuracy')
        grid_search.fit(df['postContent'], df['is_ocm'])

        # Print the best parameters and highest score
        print(f"Best parameters: {grid_search.best_params_}")
        print(f"Best cross-validation accuracy: {grid_search.best_score_}")

        # Train the best model on the entire training data
        best_model = grid_search.best_estimator_
        best_model.fit(df['postContent'], df['is_ocm'])

        # Save the best model to disk
        joblib.dump(best_model, model_output)
        print(f"Model trained and saved as {model_output}")

        # Evaluate on the test file
        df_test = pd.read_csv(test_file)
        df_test['postContent'] = df_test['postContent'].fillna('')

        # Ensure the test file has the 'is_ocm' column for evaluation
        if 'themes' in df_test.columns:
            df_test['is_ocm'] = df_test['themes'].apply(lambda theme: 1 if theme == 'Organizational Change Management' else 0)
        else:
            raise KeyError("The test file must contain a 'themes' column to create 'is_ocm' labels for evaluation.")

        predictions = best_model.predict(df_test['postContent'])
        df_test['prediction'] = predictions

        print("Classification Report on the external test set:")
        print(classification_report(df_test['is_ocm'], predictions))
        print("Accuracy on the external test set:", accuracy_score(df_test['is_ocm'], predictions))

        df_test.to_csv(test_output, index=False)
        print(f"Predictions saved to {test_output}")

    else:
        # Perform a train/test split if no test file is provided
        X_train, X_test, y_train, y_test = train_test_split(df['postContent'], df['is_ocm'], test_size=0.2, random_state=42)

        # Use GridSearchCV to find the best hyperparameters
        grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='accuracy')
        grid_search.fit(X_train, y_train)

        # Print the best parameters and highest score
        print(f"Best parameters: {grid_search.best_params_}")
        print(f"Best cross-validation accuracy: {grid_search.best_score_}")

        # Train the best model on the training data
        best_model = grid_search.best_estimator_
        best_model.fit(X_train, y_train)

        # Save the best model to disk
        joblib.dump(best_model, model_output)
        print(f"Model trained and saved as {model_output}")

        # Evaluate the model on the test set
        y_pred = best_model.predict(X_test)
        print("Classification Report on the internal test set:")
        print(classification_report(y_test, y_pred))
        print("Accuracy on the internal test set:", accuracy_score(y_test, y_pred))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a binary classifier for 'Organizational Change Management' theme.")
    parser.add_argument('train_file', type=str, help='Path to the training CSV file')
    parser.add_argument('model_output', type=str, help='Path to save the trained model')
    parser.add_argument('--test_file', type=str, help='Path to the external test CSV file', default=None)
    parser.add_argument('--test_output', type=str, help='Path to save the test predictions', default=None)

    args = parser.parse_args()
    main(args.train_file, args.model_output, args.test_file, args.test_output)

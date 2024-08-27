import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
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

def main(train_file, test_file, model_output, test_output):
    # Load the preprocessed dataset
    df = pd.read_csv(train_file)

    # Handle NaN values in 'postContent'
    df['postContent'] = df['postContent'].fillna('')

    # Define binary labels based on the themes
    df['is_pd'] = df['themes'].apply(lambda theme: 1 if theme == 'Product Development' else 0)

    # Vectorizer to transform the text data
    vectorizer = TfidfVectorizer(stop_words=stop_words, max_features=10000)

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(df['postContent'], df['is_pd'], test_size=0.2, random_state=42)

    # Build a pipeline with a classifier
    classifier = Pipeline([
        ('tfidf', vectorizer),
        ('clf', LogisticRegression(solver='liblinear'))
    ])

    # Train the model
    classifier.fit(X_train, y_train)

    # Save the classifier to disk
    joblib.dump(classifier, model_output)
    print(f"Model trained and saved as {model_output}")

    # Evaluate the model on the test set
    y_pred = classifier.predict(X_test)
    print("Classification Report on the test set:")
    print(classification_report(y_test, y_pred))
    print("Accuracy on the test set:", accuracy_score(y_test, y_pred))

    # Evaluate on the test file if provided
    if test_file:
        df_test = pd.read_csv(test_file)
        df_test['postContent'] = df_test['postContent'].fillna('')
        predictions = classifier.predict(df_test['postContent'])
        df_test['prediction'] = predictions
        df_test.to_csv(test_output, index=False)
        print(f"Predictions saved to {test_output}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a binary classifier for 'Product Development' theme.")
    parser.add_argument('train_file', type=str, help='Path to the training CSV file')
    parser.add_argument('model_output', type=str, help='Path to save the trained model')
    parser.add_argument('--test_file', type=str, help='Path to the test CSV file (optional)', default=None)
    parser.add_argument('--test_output', type=str, help='Path to save the test predictions (optional)', default='predictions.csv')

    args = parser.parse_args()
    main(args.train_file, args.test_file, args.model_output, args.test_output)

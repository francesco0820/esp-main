python sample.py csv/other.csv csv/other_120.csv 120
python combine.py csv/other_120.csv csv/regulation.csv csv/combined.csv
python split.py csv/combined.csv csv/train.csv csv/test.csv
python main.py csv/train.csv model_regulation.pkl --test_file csv/test.csv --test_output csv/predictions.csv

clf__C: This is the regularization parameter of the Logistic Regression model. A value of 10 indicates the best trade-off between bias and variance for your model.
tfidf__max_features: This parameter sets the maximum number of features (words) to consider in the TF-IDF vectorizer. 20,000 features are being used.
tfidf__ngram_range: This parameter sets the range of n-grams (word sequences) to consider. (1, 2) means both unigrams (single words) and bigrams (pairs of words) are being used.

Giving it test/train splits & not letting it split itself.
Hyperparameter Tuning:
    Added ngram_range to capture more context in the text.
    Tuned max_features and C for the TfidfVectorizer and LogisticRegression respectively.
GridSearchCV:
    Used GridSearchCV with 5-fold cross-validation to find the best hyperparameters.
    scoring='accuracy' ensures we are optimizing for accuracy.
Training the Best Model:
    Trained the best model on the entire training dataset.
    Saved the best model to disk.
Evaluation on External Test Set:
    Evaluated the model on the provided external test set.
    Printed the classification report and accuracy.
import pandas as pd
from sklearn.model_selection import train_test_split
import argparse

def split_csv(input_file, train_output, test_output, test_size=0.2, random_state=42):
    df = pd.read_csv(input_file)
    train_df, test_df = train_test_split(df, test_size=test_size, random_state=random_state)

    train_df.to_csv(train_output, index=False)
    test_df.to_csv(test_output, index=False)

    print(f"Training set saved to {train_output}")
    print(f"Test set saved to {test_output}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split a CSV file into training and test sets with an 80/20 split.")
    parser.add_argument('input_file', type=str, help='Path to the input CSV file')
    parser.add_argument('train_output', type=str, help='Path to save the training set CSV file')
    parser.add_argument('test_output', type=str, help='Path to save the test set CSV file')

    args = parser.parse_args()
    split_csv(args.input_file, args.train_output, args.test_output)

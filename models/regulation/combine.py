import pandas as pd
import argparse
from csv_utils import read_csv, write_csv, clean_text

def standardize_column_names(df):
    df.columns = [col.strip().replace(' ', '').lower() for col in df.columns]
    return df

def standardize_theme_names(df):
    theme_mapping = {
        'Regulation/Legislation': 'Regulation or Legislation'
    }
    df['theme'] = df['theme'].replace(theme_mapping)
    return df

def main(file_path_1, file_path_2, output_file_path):
    df1 = read_csv(file_path_1)
    df2 = read_csv(file_path_2)

    # Standardize column and theme names
    df1 = standardize_column_names(df1)
    df2 = standardize_column_names(df2)
    df1 = standardize_theme_names(df1)
    df2 = standardize_theme_names(df2)

    # Combine the two dataframes
    df_combined = pd.concat([df1, df2], ignore_index=True)

    # Ensure the postContent column is properly named
    if 'postcontent' in df_combined.columns:
        df_combined.rename(columns={'postcontent': 'postContent'}, inplace=True)

    # Select only the postContent and themes columns
    df_combined = df_combined[['postContent', 'theme']]

    # Clean the postContent column
    df_combined['postContent'] = df_combined['postContent'].apply(clean_text)

    # Save the combined dataframe to a new CSV file
    write_csv(df_combined, output_file_path)
    print(f'Combined CSV file saved to {output_file_path}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Combine two CSV files into one and clean postContent.")
    parser.add_argument('file_path_1', type=str, help='Path to the first CSV file')
    parser.add_argument('file_path_2', type=str, help='Path to the second CSV file')
    parser.add_argument('output_file_path', type=str, help='Path to the output CSV file')

    args = parser.parse_args()
    main(args.file_path_1, args.file_path_2, args.output_file_path)

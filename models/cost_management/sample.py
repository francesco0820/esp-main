import argparse
from csv_utils import read_csv, write_csv


def main(input_file_path, output_file_path, n_samples):
    df = read_csv(input_file_path)
    if len(df) > n_samples:
        df_sampled = df.sample(n=n_samples, random_state=1)
    else:
        df_sampled = df
    write_csv(df_sampled, output_file_path)
    print(f'Sampled CSV file saved to {output_file_path}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Take a random sample from a combined CSV file.")
    parser.add_argument('input_file_path', type=str, help='Path to the input combined CSV file')
    parser.add_argument('output_file_path', type=str, help='Path to the output sampled CSV file')
    parser.add_argument('n_samples', type=int, help='Number of samples to take')

    args = parser.parse_args()
    main(args.input_file_path, args.output_file_path, args.n_samples)

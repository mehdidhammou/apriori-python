import warnings

warnings.filterwarnings("ignore")
import pandas as pd
import sys
import os


def read_file(filename):
    """
    Reads a file based on its extension and returns a pandas DataFrame.
    Supported formats: CSV, Excel (xlsx), and JSON.
    """
    # Mapping of file extensions to pandas read functions
    read_functions = {
        ".csv": pd.read_csv,
        ".xls": pd.read_excel,
        ".xlsx": pd.read_excel,
        ".json": pd.read_json,
    }

    _, file_extension = os.path.splitext(filename)
    file_extension = file_extension.lower()

    if file_extension in read_functions:
        return read_functions[file_extension](filename, header=None)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")


def main(filename):

    try:
        df = read_file(filename)

        # Binarize the transactions
        binarized_df = (
            pd.get_dummies(df.stack(), prefix="", prefix_sep="").groupby(level=0).max()
        )

        # Convert True and False to 1 and 0
        binarized_df = binarized_df.replace({True: 1, False: 0})

        # Create a new filename by appending "_binarized" before the file extension
        base_name, extension = os.path.splitext(filename)
        new_name = f"{base_name}_binarized{extension}"

        # Save to CSV file
        binarized_df.to_csv(new_name, index=False, header=True)

        print(f"Binarized file '{new_name}' created successfully!")
    except ValueError as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    # Check if the filename was passed as an argument
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <filename>")
        sys.exit(1)

    main(sys.argv[1])

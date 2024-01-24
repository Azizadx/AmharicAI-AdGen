import sys
import os
import pandas as pd
rpath = os.path.abspath("..")
if rpath not in sys.path:
    sys.path.insert(0, rpath)
from scripts.util import Util

class DataParser:
    def __init__(self, raw_dir, parsed_dir):
        self.raw_dir = raw_dir
        self.parsed_dir = parsed_dir
        self.util = Util()
        

    def read_and_parse_files(self):
        parsed_data_list = []

        # Iterate over files in the raw directory
        for filename in os.listdir(self.raw_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(self.raw_dir, filename)

                # Read file
                data = self.util.read_file(file_path)

                # Parse messages
                parsed_message = self.util.parse_messages(data['messages'])
                parsed_data_list.append(parsed_message)

        return parsed_data_list

    def create_dataframe(self, parsed_data_list):
        # Concatenate parsed data from multiple files into a single DataFrame
        df = pd.concat([pd.DataFrame(parsed_data) for parsed_data in parsed_data_list], ignore_index=True)
        df.set_index('id', inplace=True)
        return df

    def save_dataframe(self, dataframe):
        # Save DataFrame to CSV
        dataframe.to_csv(os.path.join(self.parsed_dir, "merged_data.csv"))


if __name__ == "__main__":
    # Input: Provide the raw directory containing multiple JSON files
    raw_dir = "../data/raw"
    parsed_dir = "../data/parsed"

    # Create an instance of DataParser
    data_parser = DataParser(raw_dir, parsed_dir)

    # Read and parse files
    parsed_data_list = data_parser.read_and_parse_files()

    # Create DataFrame
    df = data_parser.create_dataframe(parsed_data_list)

    # Save DataFrame
    data_parser.save_dataframe(df)

# Import necessary modules
import sys
import os
import pandas as pd
rpath = os.path.abspath("..")
if rpath not in sys.path:
    sys.path.insert(0, rpath)
from scripts.util import Util  # Assuming Util is a class in the scripts.util module

class TextCleaner:
    def __init__(self, parsed_dir, cleaned_dir, file_name):
        self.parsed_dir = parsed_dir
        self.cleaned_dir = cleaned_dir
        self.file_name = file_name
        self.util = Util()

    def load_parsed_data(self):
        # Load parsed data
        df = pd.read_csv(f"{self.parsed_dir}/{self.file_name}.csv", index_col='id')
        return df

    def remove_null_values(self, df):
        # Remove null values
        df = df.dropna()
        return df

    def remove_newline(self, df):
        # Remove new line
        df['text'] = df['text'].replace('\n', ' ', regex=True)
        return df

    def process_hashtags(self, df):
        # Extract and remove hashtags
        df['hashtags'] = df['text'].apply(lambda x: self.util.extract_hashtags(x))
        df['text'] = df['text'].str.replace(r'\#\w+', '', regex=True)
        return df

    def process_emojis(self, df):
        # Extract and remove emojis
        df['emojis'] = df['text'].apply(self.util.extract_emojis)
        df['text'] = df['text'].apply(self.util.remove_emojis)
        return df

    def replace_letters(self, df):
        # Replace specified letters
        letters = [
            [['ሐ', 'ሑ', 'ሒ', 'ሓ', 'ሔ', 'ሖ'], ['ሀ', 'ሁ', 'ሂ', 'ሃ', 'ሄ', 'ህ', 'ሆ']],
            [['ኀ', 'ኁ', 'ኂ', 'ኃ', 'ኄ', 'ኅ', 'ኆ'], ['ሀ', 'ሁ', 'ሂ', 'ሃ', 'ሄ', 'ህ', 'ሆ']],
            [['ሠ', 'ሡ', 'ሢ', 'ሣ', 'ሤ', 'ሦ', 'ሦ', 'ሧ'], ['ሰ', 'ሱ', 'ሲ', 'ሳ', 'ሴ', 'ስ', 'ሶ', 'ሷ']],
            [['ዐ', 'ዑ', 'ዒ', 'ዓ', 'ዔ', 'ዕ', 'ዖ'], ['አ', 'ኡ', 'ኢ', 'ኣ', 'ኤ', 'እ', 'ኦ']],
            [['ጸ', 'ጹ', 'ጺ', 'ጻ', 'ጼ', 'ጽ', 'ጾ'], ['ፀ', 'ፁ', 'ፂ', 'ፃ', 'ፄ', 'ፅ', 'ፆ']]
        ]
        for letter in letters:
            for i in range(len(letter[0])):
                df['text'] = df['text'].str.replace(letter[0][i], letter[1][i])
        return df

    def process_symbols(self, df):
        # Extract and remove symbols
        df['symbols'] = df['text'].apply(self.util.extract_symbols)
        df['text'] = df['text'].apply(self.util.remove_symbols)
        return df

    def process_links(self, df):
        # Extract and remove links
        df['links'] = df['text'].apply(self.util.extract_urls)
        df['text'] = df['text'].str.replace(self.util.url_pattern, '', regex=True).str.strip()
        return df

    def process_mentions(self, df):
        # Extract and remove mentions
        df['mentions'] = df['text'].apply(self.util.extract_mentions)
        df['text'] = df['text'].str.replace(self.util.mention_pattern, '', regex=True).str.strip()
        return df

    def remove_extra_spaces(self, df):
        # Remove extra spaces
        df['text'] = df['text'].str.replace('\s+', ' ', regex=True).str.strip()
        df['text'] = df['text'].replace(r'!+', '!', regex=True)
        df['text'] = df['text'].replace(r'\.+', '', regex=True)
        return df

    def save_cleaned_data(self, df):
        # Save cleaned dataframe to CSV
        df.to_csv(f"{self.cleaned_dir}/{self.file_name}.csv", index=False)

        # Save cleaned text to .txt file
        df['text'].to_csv(f"{self.cleaned_dir}/{self.file_name}.txt", index=False, header=False)

    def clean_data(self, df):
        # Data cleaning process
        df = self.remove_null_values(df)
        df = self.remove_newline(df)
        df = self.process_hashtags(df)
        df = self.process_emojis(df)
        df = self.replace_letters(df)
        df = self.process_symbols(df)
        df = self.process_links(df)
        df = self.process_mentions(df)
        df = self.remove_extra_spaces(df)
        return df

if __name__ == "__main__":
    # Initialize variables
    parsed_dir = "../data/parsed"
    cleaned_dir = "../data/cleaned"
    file_name = "merged_data"

    # Create TextCleaner instance
    text_cleaner = TextCleaner(parsed_dir, cleaned_dir, file_name)

    # Load and clean data
    parsed_df = text_cleaner.load_parsed_data()
    cleaned_df = text_cleaner.clean_data(parsed_df)

    # Save cleaned data
    text_cleaner.save_cleaned_data(cleaned_df)

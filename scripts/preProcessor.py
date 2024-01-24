import pandas as pd
import re
from util import Util
import sys
import os
from util import Util

class DataPreProcessor:
    def __init__(self, parsed_dir, cleaned_dir, file_name):
        self.parsed_dir = parsed_dir
        self.cleaned_dir = cleaned_dir
        self.file_name = file_name
        self.util = Util()

    def clean_text(self, text):
        # Remove new line
        text = text.replace('\n', ' ')

        # Extract and remove hashtags
        hashtags = self.util.extract_hashtags(text)
        text = re.sub(r'\#\w+', '', text)

        # Extract emojis using regex
        emojis = self.util.extract_emojis(text)
        text = self.util.remove_emojis(text)

        # Replace letters
        letters = [
            [['ሐ', 'ሑ', 'ሒ', 'ሓ', 'ሔ', 'ሖ'], ['ሀ', 'ሁ', 'ሂ', 'ሃ', 'ሄ', 'ህ', 'ሆ']],
            [['ኀ', 'ኁ', 'ኂ', 'ኃ', 'ኄ', 'ኅ', 'ኆ'], ['ሀ', 'ሁ', 'ሂ', 'ሃ', 'ሄ', 'ህ', 'ሆ']],
            [['ሠ', 'ሡ', 'ሢ', 'ሣ', 'ሤ', 'ሦ', 'ሦ', 'ሧ'], ['ሰ', 'ሱ', 'ሲ', 'ሳ', 'ሴ', 'ስ', 'ሶ', 'ሷ']],
            [['ዐ', 'ዑ', 'ዒ', 'ዓ', 'ዔ', 'ዕ', 'ዖ'], ['አ', 'ኡ', 'ኢ', 'ኣ', 'ኤ', 'እ', 'ኦ']],
            [['ጸ', 'ጹ', 'ጺ', 'ጻ', 'ጼ', 'ጽ', 'ጾ'], ['ፀ', 'ፁ', 'ፂ', 'ፃ', 'ፄ', 'ፅ', 'ፆ']]
        ]
        for letter in letters:
            for i in range(len(letter[0])):
                text = text.replace(letter[0][i], letter[1][i])

        # Extract symbols
        symbols = self.util.extract_symbols(text)
        text = self.util.remove_symbols(text)

        # Extract Links
        links = self.util.extract_urls(text)

        # Remove links
        text = re.sub(self.util.url_pattern, '', text).strip()

        # Extract mentions
        mentions = self.util.extract_mentions(text)
        text = re.sub(self.util.mention_pattern, '', text).strip()

        # Remove extra spaces
        text = re.sub('\s+', ' ', text).strip()
        text = re.sub(r'!+', '!', text)
        text = re.sub(r'\.+', '', text)

        return {
            'clean_text': text,
            'hashtags': hashtags,
            'emojis': emojis,
            'letters_replaced': letters,
            'symbols': symbols,
            'links': links,
            'mentions': mentions
        }

    def process_and_save_data(self):
        # Read parsed data
        df = pd.read_csv(f"{self.parsed_dir}/{self.file_name}.csv", index_col='id')

        # Remove null values
        df = df.dropna()

        # Apply the clean_text function to the 'text' column
        df['cleaned_data'] = df['text'].apply(self.clean_text)

        # Save cleaned dataframe
        df.to_csv(f"{self.cleaned_dir}/{self.file_name}.csv")

        # Save to .txt file
        df['cleaned_data']['clean_text'].to_csv(f"{self.cleaned_dir}/{self.file_name}.txt", index=False, header=False)


# Example of usage:
#parsed_dir = "../data/parsed"
#cleaned_dir = "../data/cleaned"
#file_name = "TIKVAH"

#processor = DataPreProcessor(parsed_dir, cleaned_dir, file_name)
#processor.process_and_save_data()

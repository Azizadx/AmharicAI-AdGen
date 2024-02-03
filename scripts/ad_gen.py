import os
import pandas as pd
from math import ceil
import torch
import time
from datasets import Dataset
from transformers import AutoTokenizer, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from huggingface_hub import login
from train_utils import (
    load_model,
    create_prompt_formats,
    get_max_length,
    preprocess_dataset,
    train_model,
    generate_advertisement,
    split_train_test,
)

def main():
    dataset = load_and_preprocess_dataset()
    model, tokenizer = load_model()
    train_model(model, tokenizer, dataset)
    generate_advertisement(model, tokenizer)

def load_and_preprocess_dataset():
    file_path = "/home/nasrallah_hassan/AmharicAI-AdGen/data/parsed/Ads - adds.csv"
    df = pd.read_csv(file_path)
    dataset = df[['text', 'label']]

    dataset['text'] = dataset['text'].astype(str)
    data_dict = {"text": dataset['text'].tolist(), "label": dataset['label'].tolist()}
    dataset = Dataset.from_dict(data_dict)

    total_indices = len(dataset)
    train_dataset, test_dataset = split_train_test(dataset, total_indices)

    return train_dataset, test_dataset

if __name__ == "__main__":
    main()

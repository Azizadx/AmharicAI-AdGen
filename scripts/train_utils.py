from functools import partial
from math import ceil
import random
from datasets import Dataset
from transformers import AutoTokenizer, DataCollatorForLanguageModeling
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from transformers import AutoModelForCausalLM, AutoPeftModelForCausalLM, BitsAndBytesConfig
from bitsandbytes import nn
import torch

def load_model(model_name, bnb_config):
    n_gpus = torch.cuda.device_count()
    max_memory = f'{23000}MB'

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,
        device_map="auto",
        max_memory={i: max_memory for i in range(n_gpus)},
        trust_remote_code=True
    )

    tokenizer = AutoTokenizer.from_pretrained("misge10/amharic-tokenizer", use_auth_token=True)
    tokenizer.pad_token = tokenizer.eos_token

    return model, tokenizer

def create_prompt_formats(sample):
    INTRO_BLURB = f"Generate a persuasive and engaging advertisements for {sample['label']} in Amharic"
    RESPONSE_KEY = "Advertisement:"
    END_KEY = "### End"

    blurb = f"{INTRO_BLURB}\n\n"
    response = f"{RESPONSE_KEY}\n{sample['text']}\n\n"
    end = f"{END_KEY}"

    formatted_prompt = blurb + response + end
    sample["text"] = formatted_prompt

    return sample

def get_max_length(model):
    conf = model.config
    max_length = None
    for length_setting in ["n_positions", "max_position_embeddings", "seq_length"]:
        max_length = getattr(model.config, length_setting, None)
        if max_length:
            print(f"Found max length: {max_length}")
            break
    if not max_length:
        max_length = 1024
        print(f"Using default max length: {max_length}")
    return max_length

def preprocess_batch(batch, tokenizer, max_length):
    return tokenizer(
        batch["text"],
        max_length=max_length,
        truncation=True,
    )

def preprocess_dataset(tokenizer, max_length: int, seed, dataset):
    print("Preprocessing dataset...")
    dataset = dataset.map(create_prompt_formats)

    _preprocessing_function = partial(preprocess_batch, max_length=max_length, tokenizer=tokenizer)
    dataset = dataset.map(
        _preprocessing_function,
        batched=True,
        remove_columns=["text", "label"],
    )

    dataset = dataset.filter(lambda sample: len(sample["input_ids"]) < max_length)

    dataset = dataset.shuffle(seed=seed)

    return dataset

def create_bnb_config():
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
    )

    return bnb_config

def create_peft_config(modules):
    config = LoraConfig(
        r=16,
        lora_alpha=64,
        target_modules=modules,
        lora_dropout=0.1,
        bias="none",
        task_type="CAUSAL_LM",
    )

    return config

def find_all_linear_names(model):
    cls = nn.Linear4bit
    lora_module_names = set()
    for name, module in model.named_modules():
        if isinstance(module, cls):
            names = name.split('.')
            lora_module_names.add(names[0] if len(names) == 1 else names[-1])

    if 'lm_head' in lora_module_names:
        lora_module_names.remove('lm_head')
    return list(lora_module_names)

def print_trainable_parameters(model, use_4bit=False):
    trainable_params = 0
    all_param = 0
    for _, param in model.named_parameters():
        num_params = param.numel()

        if num_params == 0 and hasattr(param, "ds_numel"):
            num_params = param.ds_numel

        all_param += num_params
        if param.requires_grad:
            trainable_params += num_params
    if use_4bit:
        trainable_params /= 2
    print(
        f"all params: {all_param:,d} || trainable params: {trainable_params:,d} || trainable%: {100 * trainable_params / all_param}"
    )

def split_train_test(dataset, total_indices):
    random.seed(50)
    train_size = ceil(0.8 * total_indices)
    train_indices = random.sample(range(total_indices), train_size)
    test_indices = [i for i in range(total_indices) if i not in train_indices]
    train_dataset = dataset.select(train_indices)
    test_dataset = dataset.select(test_indices)

    return train_dataset, test_dataset

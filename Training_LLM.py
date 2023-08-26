from transformers import GPT2Tokenizer, GPT2LMHeadModel, DataCollatorForLanguageModeling, TrainingArguments, Trainer, LineByLineTextDataset
from transformers import GPT2Tokenizer
import os
# from transformers import GPT2Tokenizer

# from transformers import GPT2Tokenizer, GPT2LMHeadModel, DataCollatorForLanguageModeling, TrainingArguments, Trainer, LineByLineTextDataset

training_args = TrainingArguments(
    output_dir="./results",
    overwrite_output_dir=True,
    num_train_epochs=10,
    per_device_train_batch_size=32,
    per_device_eval_batch_size=64,
    eval_steps=1000,
    save_steps=1000,
    logging_dir="./logs",
)
tokenizer = GPT2Tokenizer(vocab_file="vocab.json", merges_file="merges.txt")
from transformers import GPT2TokenizerFast

tokenizer = GPT2TokenizerFast.from_pretrained("gpt2-medium")
tokenizer.pad_token = tokenizer.eos_token


tokenizer.pad_token = "<pad>"


import os
from transformers import GPT2LMHeadModel, GPT2TokenizerFast, DataCollatorForLanguageModeling, Trainer

# Load the GPT-2 model and tokenizer
model = GPT2LMHeadModel.from_pretrained("gpt2-medium")
tokenizer = GPT2TokenizerFast.from_pretrained("gpt2-medium")
tokenizer.pad_token = tokenizer.eos_token

# Custom Dataset to handle multiple files
class MultiFileTextDataset(LineByLineTextDataset):
    def __init__(self, tokenizer, filepaths, block_size):
        assert all([os.path.isfile(path) for path in filepaths]), "Some file paths are invalid."
        lines = []
        for path in filepaths:
            with open(path, "r", encoding="utf-8") as f:
                lines.extend(f.readlines())
        batch_encoding = tokenizer(lines, add_special_tokens=True, truncation=True, max_length=block_size)["input_ids"]
        self.examples = batch_encoding

# List of your .txt files
filepaths = [
    os.path.join("datasets", filename) for filename in os.listdir("datasets") if filename.endswith(".txt")
]

# Splitting the dataset into training and validation sets
split_idx = int(0.9 * len(filepaths))
filepaths_train = filepaths[:split_idx]
filepaths_valid = filepaths[split_idx:]

train_dataset = MultiFileTextDataset(tokenizer=tokenizer, filepaths=filepaths_train, block_size=128)
valid_dataset = MultiFileTextDataset(tokenizer=tokenizer, filepaths=filepaths_valid, block_size=128)

data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

# Trainer
trainer = Trainer(
    model=model,
    data_collator=data_collator,
    train_dataset=train_dataset,
    eval_dataset=valid_dataset,
)

# Train the model
trainer.train()

# Save the model
model.save_pretrained("./custom_gpt2")
tokenizer.save_pretrained("./custom_gpt2")


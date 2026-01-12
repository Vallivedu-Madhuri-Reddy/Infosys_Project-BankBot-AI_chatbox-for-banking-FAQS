# nlu_engine/train_intent.py
# Fully compatible with older Transformers versions

import os
import json
import argparse
from pathlib import Path
from sklearn.model_selection import train_test_split
from transformers import (
    DistilBertTokenizerFast,
    DistilBertForSequenceClassification,
    Trainer,
    TrainingArguments,
)
import torch
from torch.utils.data import Dataset


class IntentDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key in self.encodings}
        item["labels"] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)


def load_intents(intents_path):
    with open(intents_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    texts = []
    labels = []
    label2id = {}

    for i, intent in enumerate(data["intents"]):
        name = intent["name"]
        label2id[name] = i
        for ex in intent["examples"]:
            texts.append(ex)
            labels.append(i)

    return texts, labels, label2id


def train(args):
    print(f"Loading intents from: {args.intents}")

    texts, labels, label2id = load_intents(args.intents)
    id2label = {v: k for k, v in label2id.items()}

    print(f"Loaded {len(texts)} examples across {len(label2id)} classes.")

    # split
    train_texts, val_texts, train_labels, val_labels = train_test_split(
        texts, labels, test_size=0.2, random_state=42
    )
    print(f"Train size: {len(train_texts)}  Val size: {len(val_texts)}")

    tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")

    train_enc = tokenizer(train_texts, truncation=True, padding=True)
    val_enc = tokenizer(val_texts, truncation=True, padding=True)

    train_dataset = IntentDataset(train_enc, train_labels)
    val_dataset = IntentDataset(val_enc, val_labels)

    model = DistilBertForSequenceClassification.from_pretrained(
        "distilbert-base-uncased",
        num_labels=len(label2id),
        id2label=id2label,
        label2id=label2id,
    )

    # VERY COMPATIBLE TrainingArguments → NO evaluation or save strategies
    training_args = TrainingArguments(
        output_dir=args.output_dir,
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        learning_rate=args.lr,
        logging_steps=10,
        evaluation_strategy="no",   # <-- COMPATIBLE WITH ALL VERSIONS
        save_strategy="no",         # <-- prevents load_best_model errors
        report_to="none",
        disable_tqdm=False,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
    )

    print("Training starting...")
    trainer.train()
    print("Training completed.")

    os.makedirs(args.output_dir, exist_ok=True)
    trainer.save_model(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)
    print(f"Model saved at {args.output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--intents")
    parser.add_argument("--output_dir")
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch_size", type=int, default=16)
    parser.add_argument("--lr", type=float, default=5e-5)

    args = parser.parse_args()
    train(args)


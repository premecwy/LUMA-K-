import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import json
import os

MODEL_DIR = os.path.join(os.path.dirname(__file__), "../model")

tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR, use_fast=False)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
model.eval()

with open(os.path.join(MODEL_DIR, "label_names.json"), encoding="utf-8") as f:
    label_names = json.load(f)

def predict_label(text: str, threshold: float = 0.5):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.sigmoid(outputs.logits).squeeze().numpy()

    labels = [label_names[i] for i, p in enumerate(probs) if p >= threshold]
    return labels, probs.tolist()

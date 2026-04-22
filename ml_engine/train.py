import csv
import json
import os
import re
from collections import defaultdict
import math

def tokenize(text):
    text = text.lower()
    # Find all words (alphanumeric sequences)
    words = re.findall(r'\b\w+\b', text)
    # Simple stopword list
    stopwords = {"the", "is", "at", "which", "on", "a", "an", "and", "in", "to", "of", "for", "with", "it", "this"}
    return [word for word in words if word not in stopwords]

def train_naive_bayes():
    dataset_path = os.path.join(os.path.dirname(__file__), 'dataset.csv')
    model_dir = os.path.join(os.path.dirname(__file__), 'model')
    
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    # Class distribution and vocabulary
    class_counts = defaultdict(int)
    word_counts = {'phishing': defaultdict(int), 'legitimate': defaultdict(int)}
    total_words = {'phishing': 0, 'legitimate': 0}
    vocab = set()

    # Read data
    num_docs = 0
    with open(dataset_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            text = row.get('text', '')
            label = row.get('label', '')
            if not text or not label:
                continue
            
            num_docs += 1
            class_counts[label] += 1
            
            tokens = tokenize(text)
            
            # Additional feature: Presence of URL
            has_link = bool(re.search(r'http[s]?://', text))
            if has_link:
                tokens.append("__URL__")
                
            for word in tokens:
                word_counts[label][word] += 1
                total_words[label] += 1
                vocab.add(word)

    # Calculate probabilities
    model = {
        'classes': {},
        'vocab_size': len(vocab),
        'prior': {}
    }

    # Priors
    for label, count in class_counts.items():
        model['prior'][label] = count / num_docs
        
    # Word Probs (Log probabilities with Laplace smoothing)
    for label in class_counts.keys():
        model['classes'][label] = {}
        denom = total_words[label] + len(vocab)
        for word in vocab:
            count = word_counts[label].get(word, 0) + 1  # Laplace smoothing (Add-1)
            model['classes'][label][word] = math.log(count / denom)
            
        # Unknown word probability (for words not in vocab during inference)
        model['classes'][label]['__UNKNOWN__'] = math.log(1 / denom)

    # Save the model
    model_path = os.path.join(model_dir, 'model.json')
    with open(model_path, 'w', encoding='utf-8') as f:
        json.dump(model, f, indent=2)
        
    print(f"Model successfully trained on {num_docs} documents.")
    print(f"Vocabulary size: {len(vocab)}")
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    train_naive_bayes()

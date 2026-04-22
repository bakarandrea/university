import json
import os
import re
import math

def tokenize(text):
    text = text.lower()
    words = re.findall(r'\b\w+\b', text)
    stopwords = {"the", "is", "at", "which", "on", "a", "an", "and", "in", "to", "of", "for", "with", "it", "this"}
    return [word for word in words if word not in stopwords]

def load_model():
    model_path = os.path.join(os.path.dirname(__file__), 'model', 'model.json')
    if not os.path.exists(model_path):
        return None
    with open(model_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Keep model in memory
_model_cache = load_model()

def predict_text(text):
    if not _model_cache:
        raise Exception("Model not trained. Please run train.py first.")
        
    tokens = tokenize(text)
    
    # Feature engineering similar to train
    has_link = bool(re.search(r'http[s]?://', text))
    if has_link:
        tokens.append("__URL__")
        
    scores = {}
    
    # Calculate sum of log probabilities
    for label in _model_cache['classes'].keys():
        # Start with log of prior probability
        score = math.log(_model_cache['prior'][label])
        
        for word in tokens:
            # Add log prob of word given class
            word_log_prob = _model_cache['classes'][label].get(word, _model_cache['classes'][label]['__UNKNOWN__'])
            score += word_log_prob
            
        scores[label] = score
        
    # Convert log probs to actual probabilities safely (using log-sum-exp trick)
    max_log_score = max(scores.values())
    probs = {}
    sum_exp = 0
    for label, log_score in scores.items():
        # Shift to prevent underflow
        exp_val = math.exp(log_score - max_log_score)
        probs[label] = exp_val
        sum_exp += exp_val
        
    # Normalize
    for label in probs:
        probs[label] = (probs[label] / sum_exp) * 100
        
    # Find prediction
    prediction = max(probs, key=probs.get)
    confidence = probs[prediction]
    
    return {
        'prediction': prediction,
        'confidence': round(confidence, 2),
        'probabilities': {k: round(v, 2) for k, v in probs.items()}
    }

if __name__ == "__main__":
    sample_text = "Claim your free iPhone 15 now! Limited time offer, click http://free-iphone-claim.com"
    print(f"Text: {sample_text}")
    print(predict_text(sample_text))

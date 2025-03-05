import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import numpy as np
import json

np.random.seed(41)

# Load the CSV files into pandas DataFrames
mes_data = pd.read_csv("data/MES-Medical Expenditure System.csv")
cas_data = pd.read_csv("data/CAS-Credit Approval System.csv")

# Convert Expected Output to integers where values starting with '1' are 1, others are 0
mes_data['Expected Output'] = mes_data['Expected Output'].apply(lambda x: 1 if str(x).startswith('1') else 0)
cas_data['Expected Output'] = cas_data['Expected Output'].apply(lambda x: 1 if str(x).startswith('1') else 0)

def compute_metrics(data):
    y_true = data['Expected Output']
    models = ['GPT-3.5', 'GPT-4', 'DoXpert']
    
    # Initialize dictionaries to store metrics
    precision = {}
    recall = {}
    f1 = {}
    accuracy = {}

    # Metrics for always 1
    precision['Always Yes (1)'] = precision_score(y_true, np.ones_like(y_true))
    recall['Always Yes (1)'] = recall_score(y_true, np.ones_like(y_true))
    f1['Always Yes (1)'] = f1_score(y_true, np.ones_like(y_true))
    accuracy['Always Yes (1)'] = accuracy_score(y_true, np.ones_like(y_true))
    
    # Metrics for always 0 (only precision is meaningful, others will avoid division by zero)
    precision['Always No (0)'] = precision_score(y_true, np.zeros_like(y_true))
    recall['Always No (0)'] = recall_score(y_true, np.zeros_like(y_true))
    f1['Always No (0)'] = f1_score(y_true, np.zeros_like(y_true))
    accuracy['Always No (0)'] = accuracy_score(y_true, np.zeros_like(y_true))
    
    # Random predictions
    random_predictions = np.random.randint(2, size=len(y_true))
    precision['Random'] = precision_score(y_true, random_predictions)
    recall['Random'] = recall_score(y_true, random_predictions)
    f1['Random'] = f1_score(y_true, random_predictions)
    accuracy['Random'] = accuracy_score(y_true, random_predictions)
    
    # Calculate metrics for each model
    for model in models:
        precision[model] = precision_score(y_true, data[model])
        recall[model] = recall_score(y_true, data[model])
        f1[model] = f1_score(y_true, data[model])
        accuracy[model] = accuracy_score(y_true, data[model])
    
    return {'Precision': precision, 'Recall': recall, 'F1 Score': f1, 'Accuracy': accuracy}

# Compute metrics for both datasets
mes_metrics = compute_metrics(mes_data)
cas_metrics = compute_metrics(cas_data)

print('MES:', json.dumps(mes_metrics, indent=4))
print('CAS:', json.dumps(cas_metrics, indent=4))

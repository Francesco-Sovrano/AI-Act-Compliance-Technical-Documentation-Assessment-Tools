import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import json

def calculate_differences(df):
    """
    Calculate the differences between the columns and "Majority Vote".
    """
    # Convert to "Y" or "N" based on the first character
    columns = ['Majority Vote', 'Answer / ChatGPT 4', 'Answer / ChatGPT 3.5', 'Answer / DoX', 'Correct Answer']
    for col in columns:
        df[col] = df[col].apply(lambda x: 'Y' if str(x).strip()[0] == 'Y' else 'N')
    
    # Compute differences
    results = {
        'Answer / ChatGPT 4': sum(df['Answer / ChatGPT 4'] != df['Majority Vote']),
        'Answer / ChatGPT 3.5': sum(df['Answer / ChatGPT 3.5'] != df['Majority Vote']),
        'Answer / DoX': sum(df['Answer / DoX'] != df['Majority Vote']),
        'Constant Y': sum(df['Majority Vote'] == 'N'),
        'Constant N': sum(df['Majority Vote'] == 'Y'),
    }
    df['Constant Y'] = 'Y'
    df['Constant N'] = 'N'

    # Add differences for random choices
    np.random.seed(42)
    df['Random'] = np.random.choice(['Y', 'N'], size=len(df))
    results['Random'] = sum(df['Random'] != df['Majority Vote'].to_numpy())
    
    return results

# Load the CSV files
credit_approval_df = pd.read_csv('data/credit_approval_system.csv')
# print(len(credit_approval_df))
medical_expenditure_df = pd.read_csv('data/medical_expenditure_system.csv')
# print(len(medical_expenditure_df))

# # Filter out rows where 'Interpersonal Agreement' is equal to 'N'
# credit_approval_df = credit_approval_df[credit_approval_df['Interpersonal Agreement'] != 'N']
# medical_expenditure_df = medical_expenditure_df[medical_expenditure_df['Interpersonal Agreement'] != 'N']

# Calculate differences for each dataframe
credit_approval_diff = calculate_differences(credit_approval_df)
medical_expenditure_diff = calculate_differences(medical_expenditure_df)

# Convert absolute differences to percentages for visualization
credit_approval_total = len(credit_approval_df)
medical_expenditure_total = len(medical_expenditure_df)

credit_approval_diff_percent = {
    k: (v / credit_approval_total) * 100
    for k,v in credit_approval_diff.items()
}

medical_expenditure_diff_percent = {
    k: (v / medical_expenditure_total) * 100
    for k,v in medical_expenditure_diff.items()
}

# Plotting the updated differences with larger fonts and added annotations
plt.figure(figsize=(10, 8))

# Data to plot
labels = ['Credit Approval', 'Medical Expenditure']
bar_width = 0.2
index = [0, 1.35]  # Adjust the 1.5 for more or less space
dox_differences = [credit_approval_diff_percent['Answer / DoX'], medical_expenditure_diff_percent['Answer / DoX']]
chatgpt_differences = [credit_approval_diff_percent['Answer / ChatGPT 3.5'], medical_expenditure_diff_percent['Answer / ChatGPT 3.5']]
chatgpt4_differences = [credit_approval_diff_percent['Answer / ChatGPT 4'], medical_expenditure_diff_percent['Answer / ChatGPT 4']]
constant_y_differences = [credit_approval_diff_percent['Constant Y'], medical_expenditure_diff_percent['Constant Y']]
constant_n_differences = [credit_approval_diff_percent['Constant N'], medical_expenditure_diff_percent['Constant N']]
random_differences = [credit_approval_diff_percent['Random'], medical_expenditure_diff_percent['Random']]

# Create bars
bar1 = plt.bar(index, dox_differences, bar_width, label='DoXpert', color='b', alpha=0.7)
bar2 = plt.bar([i + bar_width for i in index], chatgpt_differences, bar_width, label='ChatGPT-3.5', color='r', alpha=0.7)
bar3 = plt.bar([i + 2*bar_width for i in index], chatgpt4_differences, bar_width, label='ChatGPT-4', color='y', alpha=0.7)
bar4 = plt.bar([i + 3*bar_width for i in index], constant_y_differences, bar_width, label='Constant Y', color='g', alpha=0.7)
bar5 = plt.bar([i + 4*bar_width for i in index], constant_n_differences, bar_width, label='Constant N', color='m', alpha=0.7)
bar6 = plt.bar([i + 5*bar_width for i in index], random_differences, bar_width, label='Random', color='c', alpha=0.7)

# Add annotations on top of each bar
for idx, rect in enumerate(bar1):
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width()/2., height + 0.15, '%.2f%%' % height, ha='center', va='bottom', fontsize=16)

for idx, rect in enumerate(bar2):
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width()/2., height + 0.15, '%.2f%%' % height, ha='center', va='bottom', fontsize=16)

for idx, rect in enumerate(bar3):
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width()/2., height + 0.15, '%.2f%%' % height, ha='center', va='bottom', fontsize=16)

for idx, rect in enumerate(bar4):
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width()/2., height + 0.15, '%.2f%%' % height, ha='center', va='bottom', fontsize=16)

for idx, rect in enumerate(bar5):
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width()/2., height + 0.15, '%.2f%%' % height, ha='center', va='bottom', fontsize=16)

for idx, rect in enumerate(bar6):
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width()/2., height + 0.15, '%.2f%%' % height, ha='center', va='bottom', fontsize=16)

# Label settings
plt.xlabel('System', fontsize=22)
plt.ylabel('Difference Percentage (%)', fontsize=22)
plt.title('Differences from Majority of Experts', fontsize=24)
plt.xticks([i + 2.5*bar_width for i in index], labels, fontsize=20)
plt.yticks(fontsize=20)
plt.legend(fontsize=20)

# Display the plot
plt.tight_layout()
plt.savefig(f'ai_vs_experts.png')

#######################
def calculate_metrics(df):
    """
    Calculate precision, recall, and accuracy for each system compared to the correct answer.
    """
    systems = ['Answer / ChatGPT 4', 'Answer / ChatGPT 3.5', 'Answer / DoX', 'Random', 'Constant Y', 'Constant N']
    metrics = {}

    for system in systems:
        true_values = df['Majority Vote']
        # print(len(true_values))
        predicted_values = df[system]

        # Calculate metrics
        accuracy = accuracy_score(true_values, predicted_values)
        precision = precision_score(true_values, predicted_values, pos_label='Y')
        recall = recall_score(true_values, predicted_values, pos_label='Y')
        f1 = f1_score(true_values, predicted_values, pos_label='Y')

        metrics[system] = {
            'Precision': precision,
            'Recall': recall,
            'Accuracy': accuracy,
            'F1': f1
        }

    return metrics

print('Credit Approval', json.dumps(calculate_metrics(credit_approval_df), indent=4))
print('Medical Expenditure', json.dumps(calculate_metrics(medical_expenditure_df), indent=4))
#########################

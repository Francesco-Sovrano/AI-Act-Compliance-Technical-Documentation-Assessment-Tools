import os
import pandas as pd
from sklearn.metrics import cohen_kappa_score
from tabulate import tabulate

data_path = './data'

# List the extracted files
extracted_files = [os.path.join(data_path, file) for file in os.listdir(data_path) if file.endswith('.csv')]

# Display the list of extracted CSV files
print(extracted_files)

# Function to calculate Cohen's Kappa and Percentage Agreement
def calculate_agreement_metrics(file_path):
	# Load the CSV file
	df = pd.read_csv(file_path)
	
	# Filter columns that start with "Answer"
	answer_columns = [col for col in df.columns if col.startswith("Answer")]
	
	# Ensure there are exactly three answer columns
	if len(answer_columns) != 3:
		raise ValueError(f"{file_path} does not have exactly three 'Answer' columns.")
	
	# Compute Cohen's Kappa and Percentage Agreement
	results = {}
	
	# Cohen's Kappa
	kappa_12 = cohen_kappa_score(df[answer_columns[0]], df[answer_columns[1]])
	kappa_13 = cohen_kappa_score(df[answer_columns[0]], df[answer_columns[2]])
	kappa_23 = cohen_kappa_score(df[answer_columns[1]], df[answer_columns[2]])
	
	# Percentage Agreement
	def percentage_agreement(col1, col2):
		return (df[col1] == df[col2]).mean()
	
	percent_agreement_12 = percentage_agreement(answer_columns[0], answer_columns[1])
	percent_agreement_13 = percentage_agreement(answer_columns[0], answer_columns[2])
	percent_agreement_23 = percentage_agreement(answer_columns[1], answer_columns[2])
	
	# Store results
	results['file'] = file_path
	results['kappa_12'] = kappa_12
	results['kappa_13'] = kappa_13
	results['kappa_23'] = kappa_23
	results['percent_agreement_12'] = percent_agreement_12
	results['percent_agreement_13'] = percent_agreement_13
	results['percent_agreement_23'] = percent_agreement_23
	
	return results

# Process each file and collect results
all_results = []
for file in extracted_files:
	results = calculate_agreement_metrics(file)
	all_results.append(results)

# Convert results to a DataFrame and display
results_df = pd.DataFrame(all_results)

print("Cohen's Kappa and Percentage Agreement", tabulate(results_df, headers='keys', tablefmt='pretty'))

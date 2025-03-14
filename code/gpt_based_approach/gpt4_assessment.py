import openai
import os
import time
from tqdm import tqdm
import sys
import pickle
import os
import types
from more_itertools import unique_everseen
import json
import csv

# Initialize OpenAI API
openai.organization = os.environ.get('OPENAI_ORGANIZATION')
openai.api_key = os.environ.get('OPENAI_API_KEY')

results_dir = 'results'
os.makedirs(results_dir, exist_ok=True)
results_dir = 'results/gpt4'
os.makedirs(results_dir, exist_ok=True)

model = 'gpt-4-0613'
max_model_input_size = 8192

# model = 'gpt-3.5-turbo-16k-0613'
# max_model_input_size = 8192*2

prompt_template = '''As a machine learning engineer and legal expert, your task is to assess the compliance of this technical documentation about an AI system based on the following question. Conduct an intermediate compliance assessment, focusing on both the technical and legal requirements.

Your assessment should start with a numerical score from 1 to 5, where 1 indicates the question is not answered at all and 5 indicates it's perfectly answered. Following the score, provide a brief explanation highlighting the strengths or weaknesses in addressing the question. Consider the completeness, clarity, and legal implications in your explanation.

For example, your assessment might look like: 
'Score: 3. Explanation: The question was only partially answered. While the technical aspects are covered, it lacks in legal disclosures.'

Question:
{q}

Technical documentation:
{p}
'''

def get_document_list(directory):
    doc_list = []
    for obj in os.listdir(directory):
        obj_path = os.path.join(directory, obj)
        if os.path.isfile(obj_path):
            doc_list.append(obj_path)
        elif os.path.isdir(obj_path):
            doc_list.extend(get_document_list(obj_path))
    return doc_list

def create_cache(file_name, create_fn):
    print(f'Creating cache <{file_name}>..')
    result = create_fn()
    with open(file_name, 'wb') as f:
        pickle.dump(result, f)
    return result

def load_cache(file_name):
    if os.path.isfile(file_name):
        print(f'Loading cache <{file_name}>..')
        with open(file_name,'rb') as f:
            return pickle.load(f)
    return None

def load_or_create_cache(file_name, create_fn):
    result = load_cache(file_name)
    if result is None:
        result = create_cache(file_name, create_fn)
    return result

def get_cached_values(value_list, cache, fetch_fn, key_fn=lambda x:x):
    if isinstance(value_list, types.GeneratorType):
        value_list = tuple(value_list)
    missing_values = tuple(
        q 
        for q in unique_everseen(filter(lambda x:x, value_list), key=key_fn) 
        if key_fn(q) not in cache
    )
    if len(missing_values) > 0:
        new_values = fetch_fn(missing_values)
        cache.update({
            key_fn(q):v 
            for q,v in zip(missing_values, new_values)
        })
        # del missing_values
        # del new_values
    return [cache[key_fn(q)] if q else None for q in value_list]

def instruct_model(prompt, temperature=0, top_p=0, frequency_penalty=0, presence_penalty=0, **kwargs):
    def fetch_fn(missing_prompt_list):
        missing_prompt = missing_prompt_list[0]
        messages = [ {"role": "user", "content": missing_prompt} ]
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            max_tokens=max_model_input_size-2*len(missing_prompt.split(' ')),
            n=1,
            # stop=None,
            temperature=temperature,
            top_p=top_p,
            frequency_penalty=frequency_penalty, 
            presence_penalty=presence_penalty,
        )
        return [response.choices[0].message.content.strip()]
    return get_cached_values([prompt], __gpt_cache, fetch_fn)[0]

gpt_cache_name = f"_{model.replace('-','_')}_cache.pkl"
__gpt_cache = load_or_create_cache(gpt_cache_name, lambda: {})

# Read checklist from txt file
with open("../../data/checklist/checklist.txt", "r") as f:
    checklist = f.readlines()

checklist = [item.strip() for item in checklist]

# Read software documentation from txt or md file
for documentation_file in filter(lambda x: x.endswith('.txt') or x.endswith('.md') or x.endswith('.html'), get_document_list('../../data/technical_docs')):
    # documentation_file = sys.argv[1]  # Change this to your documentation filename
    with open(documentation_file, "r") as f:
        documentation = f.read()

    # Split documentation into sections or chunks
    max_tokens = (max_model_input_size*2)//3 - len(prompt_template.split(' '))
    chunks = [documentation[i:i + max_tokens] for i in range(0, len(documentation.split(' ')), max_tokens)]
    print('Number of chunks:', len(chunks))

    # Initialize scores
    scores = {question: [] for question in checklist}

    # Evaluate each chunk with ChatGPT
    for question in tqdm(checklist):
        for chunk in chunks:
            prompt = prompt_template.format(q=question,p=chunk)
            # print(prompt)
            response = instruct_model(prompt)
            # create_cache(gpt_cache_name, lambda: __gpt_cache)
            score,explanation = response.split('Explanation:')
            score = score.strip()[6:].strip(';,-. ').strip()
            score = float(score)
            scores[question].append({'score':score,'explanation': explanation})
            # if model.startswith('gpt-4'):
            #     time.sleep(60)

    # Calculate average scores for each question
    for question in scores.keys():
        best_assessment = max(scores[question], key=lambda x: x['score'])
        scores[question] = [best_assessment]

    # Print results
    with open(results_dir+'/'+documentation_file.split('/')[-1]+'.results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Write header
        writer.writerow(['Question', 'Score', 'Explanation'])
        
        # Write content
        for question, assessments in scores.items():
            for assessment in assessments:
                score = assessment['score']
                explanation = assessment['explanation']
                writer.writerow([question, score, explanation])
    # print("Note: One of the limitations of this approach is that information related to a checklist question could be scattered across the documentation. This might lead to inaccurate scores.")

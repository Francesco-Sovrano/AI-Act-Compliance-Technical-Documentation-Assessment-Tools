source .env/bin/activate

################################
######## ChatGPT ###############
################################

cd code/gpt_based_approach/
python3 gpt3.5_assessment.py
python3 gpt4_assessment.py
cd ../../

################################
######## DoXpert ###############
################################

cd code/doxpert/

mkdir logs
mkdir cache

CHECKLIST_PERTINENCE_THRESHOLD=0.3
DOX_ANSWER_PERTINENCE_THRESHOLD=0.3
SYNONYMITY_THRESHOLD=0.55

#### Medical Expenditure - Final Version
mkdir cache/cache_exp3_hd_v2
python3 doxpert_assessment.py \
	--model_type fb \
	--checklist_pertinence_threshold $CHECKLIST_PERTINENCE_THRESHOLD \
	--dox_answer_pertinence_threshold $DOX_ANSWER_PERTINENCE_THRESHOLD \
	--synonymity_threshold $SYNONYMITY_THRESHOLD \
	--checklist_path ../../data/checklist/checklist.txt \
	--open_question_path ../../data/checklist/open_questions.txt \
	--explainable_information_path ../../data/technical_docs/medical_expenditure/v2 \
	--cache_path ./cache/cache_exp3_hd_v2 \
	&> ./logs/exp3.hd_v2.fb.log.txt 

#### Credit Approval System - Final Version
mkdir cache/cache_exp3_ca_v2
python3 doxpert_assessment.py \
	--model_type fb \
	--checklist_pertinence_threshold $CHECKLIST_PERTINENCE_THRESHOLD \
	--dox_answer_pertinence_threshold $DOX_ANSWER_PERTINENCE_THRESHOLD \
	--synonymity_threshold $SYNONYMITY_THRESHOLD \
	--checklist_path ../../data/checklist/checklist.txt \
	--open_question_path ../../data/checklist/open_questions.txt \
	--explainable_information_path ../../data/technical_docs/credit_approval_system/v2 \
	--cache_path ./cache/cache_exp3_ca_v2 \
	&> ./logs/exp3.ca_v2.fb.log.txt 

#### Medical Expenditure - Merged Notebooks & Tutorials
mkdir cache/cache_exp3_hd_v1
python3 doxpert_assessment.py \
	--model_type fb \
	--checklist_pertinence_threshold $CHECKLIST_PERTINENCE_THRESHOLD \
	--dox_answer_pertinence_threshold $DOX_ANSWER_PERTINENCE_THRESHOLD \
	--synonymity_threshold $SYNONYMITY_THRESHOLD \
	--checklist_path ../../data/checklist/checklist.txt \
	--open_question_path ../../data/checklist/open_questions.txt \
	--explainable_information_path ../../data/technical_docs/medical_expenditure/v1 \
	--cache_path ./cache/cache_exp3_hd_v1 \
	&> ./logs/exp3.hd_v1.fb.log.txt 

#### Credit Approval System - Merged Notebooks & Tutorials
mkdir cache/cache_exp3_ca_v1
python3 doxpert_assessment.py \
	--model_type fb \
	--checklist_pertinence_threshold $CHECKLIST_PERTINENCE_THRESHOLD \
	--dox_answer_pertinence_threshold $DOX_ANSWER_PERTINENCE_THRESHOLD \
	--synonymity_threshold $SYNONYMITY_THRESHOLD \
	--checklist_path ../../data/checklist/checklist.txt \
	--open_question_path ../../data/checklist/open_questions.txt \
	--explainable_information_path ../../data/technical_docs/credit_approval_system/v1 \
	--cache_path ./cache/cache_exp3_ca_v1 \
	&> ./logs/exp3.ca_v1.fb.log.txt 


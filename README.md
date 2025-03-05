# Simplifying Software Compliance: AI Technologies in Drafting Technical Documentation for the AI Act

Welcome to the replication package for the [EMSE](https://link.springer.com/journal/10664) paper titled *'Simplifying Software Compliance: AI Technologies in Drafting Technical Documentation for the AI Act.'*.

## Abstract

The European AI Act has introduced specific technical documentation requirements for AI systems. Compliance with them is challenging due to the need for advanced knowledge of both legal and technical aspects, which is rare among software developers and legal professionals. Consequently, small and medium-sized enterprises may face high costs in meeting these requirements. In this study, we explore how contemporary AI technologies, including ChatGPT and an existing compliance tool (DoXpert), can aid software developers in creating technical documentation that complies with the AI Act. We specifically demonstrate how these AI tools can identify gaps in existing documentation according to the provisions of the AI Act. Using open-source high-risk AI systems as case studies, we collaborated with legal experts to evaluate how closely tool-generated assessments align with expert opinions. Findings show partial alignment, important issues with ChatGPT (3.5 and 4), and a moderate (and statistically significant) correlation between DoXpert and expert judgments, according to the Rank Biserial Correlation analysis. Nonetheless, these findings underscore the potential of AI to combine with human analysis and alleviate the compliance burden, supporting the broader goal of fostering responsible and transparent AI development under emerging regulatory frameworks.

## Repository Contents

This repository comprises various tools, scripts, and data sets essential for replicating the findings of our EMSE paper. Here's a detailed breakdown:

- **code**:
  - `data_analysis`: Contains scripts dedicated to the analysis of the research data.
  - `doxpert`: Houses the source code of the DoXpert tool.
  - `gpt_based_approach`: Directory with scripts that implement the baseline tool leveraging ChatGPT.
  - `packages`: Includes custom Python packages used throughout the project which are forked versions of:
    - [DoXpy](https://github.com/Francesco-Sovrano/DoXpy)
    - [DiscoLQA](https://github.com/Francesco-Sovrano/DiscoLQA)
  
- **data**:
  - `assessment_results`: Contains the outcomes of the automated and/or human evaluations of the technical documentation.
  - `technical_docs`: Provides example technical documentation integral to the study.
    - **Credit Scoring System**: Derived from tutorials on credit scoring using Jupyter Notebooks from the AIF360 and AIX360 libraries. The repository contains two versions of the technical documentation for this system:
      1. Initial version: Obtained by merging the tutorials and notebooks.
      2. Final version: Refined after applying the DoXpert tool.
    - **Medical Expenditure System**: Originates from tutorials on medical expenditure estimation using Jupyter Notebooks from the AIF360 and AIX360 libraries. The repository houses two versions of the technical documentation for this system:
      1. Initial version: Assembled by integrating insights from both tutorials.
      2. Final version: Enhanced after the application of the DoXpert tool.
  - `checklist`: Features the checklist instrumental in evaluating the compliance of technical documentation with the AI Act.

- **setup_virtualenv.sh**: A script designed to establish a virtual environment for the project, ensuring isolation and specific dependency versions.
  
- **run_automated_assessments.sh**: A shell script crafted to execute the automated assessments elucidated in the research paper.

## System Specifications

This repository is tested and recommended on:

- OS: Linux (Debian 5.10.179 or newer) and macOS (13.2.1 Ventura or newer)
- Python version: 3.7 or newer

## Forked Repositories

This package uses forked versions of two repositories. The original repositories can be found at:
- [DoXpy Repository](https://github.com/Francesco-Sovrano/DoXpy)
- [DiscoLQA Repository](https://github.com/Francesco-Sovrano/DiscoLQA)

## Configuration and Setup

Before using the tools and scripts in this repository, you need to configure certain environment variables and potentially set up a virtual environment.

Download [pytorch_model.bin](https://zenodo.org/records/10555604/files/pytorch_model.bin?download=1) from [https://doi.org/10.5281/zenodo.10555603](https://doi.org/10.5281/zenodo.10555603) and move it inside [code/doxpert/question_extractor/data/models/distilt5-disco-qaamr-multi](code/doxpert/question_extractor/data/models/distilt5-disco-qaamr-multi).

### Environment Variables

To use this package, you must set up two environment variables: `OPENAI_ORGANIZATION` and `OPENAI_API_KEY`. These variables represent your OpenAI organization identifier and your API key respectively.



#### Setting Up Environment Variables

##### On UNIX-like Operating Systems (Linux, MacOS):

1. Open your terminal.
2. To set the `OPENAI_ORGANIZATION` variable, run:
   ```bash
   export OPENAI_ORGANIZATION='your_organization_id'
   ```
3. To set the `OPENAI_API_KEY` variable, run:
   ```bash
   export OPENAI_API_KEY='your_api_key'
   ```
4. These commands will set the environment variables for your current session. If you want to make them permanent, you can add the above lines to your shell profile (`~/.bashrc`, `~/.bash_profile`, `~/.zshrc`, etc.)

##### On Windows:

1. Press `Win + R`, type `sysdm.cpl`, and press Enter.
2. Go to the `Advanced` tab and click on `Environment Variables`.
3. Under `User variables`, click on `New`.
4. For the `Variable name` field, enter `OPENAI_ORGANIZATION` and for the `Variable value` field, enter your organization ID.
5. Repeat the process and add another user variable with the name `OPENAI_API_KEY` and your API key as the value.
6. Click `OK` to close all windows.

#### Verifying the Setup

To ensure you've set up the environment variables correctly:

1. In your terminal or command prompt, run:
   ```bash
   echo $OPENAI_ORGANIZATION  # For UNIX-like systems
   ```
   or
   ```powershell
   echo %OPENAI_ORGANIZATION%  # For Windows
   ```
   This should display your organization ID.
   
2. Similarly, verify the API key:
   ```bash
   echo $OPENAI_API_KEY  # For UNIX-like systems
   ```
   or
   ```powershell
   echo %OPENAI_API_KEY%  # For Windows
   ```

Ensure that both values match what you've set.

### Setting Up the Virtual Environment

To create a virtual environment and install necessary dependencies, run the following script:

```bash
./setup_virtualenv.sh
```

### Running Automated Assessments

After setting up the environment, you can run the automated assessments using:

```bash
./run_automated_assessments.sh
```

## Conclusion

We hope this repository serves as a valuable resource for AI practitioners aiming to align their AI systems with the AI Act's requirements. Feedback and contributions are always welcome!

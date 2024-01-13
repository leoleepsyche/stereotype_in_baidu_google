# A comparison of online search engine moderation in Google and Baidu

This repository contains the code to reproduce the results of the analysis presented in our paper: <br>
"A comparison of online search engine moderation in Google and Baidu" Geng Liu, Pietro Pinoli, Stefano Ceri, Francesco Pierri (2024).

For a detailed description of the data used in this analysis, see the [Data Description](data/README.md).

## Code Description

### 1. Data Collection
- **Script**: _0_data_collection.py_
- **Description**: Designed to fetch autocomplete suggestions from Google and Baidu search engines. This script generates a list of queries based on predefined templates and categories, retrieves autocomplete suggestions for these queries, and saves the results in CSV files.
- **Usage**:
  - Run the script to collect auto-completion data from Google and Baidu based on template queries.

### 2. Data Preprocessing and Analysis
- **Script**: _1_data_preprocess.ipynb_
- **Description**: Preprocesses and analyzes autocomplete suggestions from Google and Baidu. It identifies unresponded queries, merges them with original data, performs sentiment analysis, and saves the results.
- **Usage**:
  - Execute the script to process autocomplete suggestions from Google and Baidu.
  - Outputs processed and analyzed data in CSV files.
- **Note**:
  - This script includes API calls for Baidu translation and OpenAI for sentiment analysis. Ensure you use your own API keys.

### 3. Replication of Analysis
- **Script**: _2_replication_analysis.ipynb_
- **Description**: Provides a comprehensive analysis of autocomplete suggestions from Google and Baidu, including consistency of suggestions, unresponded queries, and sentiment analysis as detailed in our paper.
- **Usage**:
  - Run the script to replicate our analysis.
- **Note**:
  - Ensure the correct file paths are set according to your directory structure.
  - The script handles data cleaning, processing, and visualization. Review and modify it as necessary to fit your specific data and analysis requirements.


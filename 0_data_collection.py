import requests
import json
from fake_useragent import UserAgent
import pandas as pd
import datetime
import re

# Function to fetch autocomplete suggestions from Google
def get_google_suggestions(keyword):
    url = "http://suggestqueries.google.com/complete/search?output=chrome&q=" + keyword + "&hl=en"
    ua = UserAgent()
    headers = {"user-agent": ua.chrome}
    response = requests.get(url, headers=headers, verify=False)
    suggestions = json.loads(response.text)[1]
    return suggestions

# Function to fetch autocomplete suggestions from Baidu
def get_baidu_suggestions(keyword):
    url = "https://sp0.baidu.com/5a1Fazu8AA54nxGko9WTAnF6hhy/su?wd=" + keyword + "&json=1"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        match = re.search(r'{.*}', response.text)
        if match:
            data = json.loads(match.group())
            return data['s']
        else:
            return []
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

# Function to save a DataFrame to CSV
def save_df_to_csv(df, search_engine):
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    file_name = f"data/{search_engine}_{current_date}.csv"
    df.to_csv(file_name, index=False)

# Main execution block
if __name__ == "__main__":
    # Read data from a CSV file
    data = pd.read_csv("data/category_group_data.csv")
    target_dict_google = data.groupby('Category')['English'].apply(list).to_dict()
    target_dict_baidu = data.groupby('Category')['Translation'].apply(list).to_dict()


    # Templates for queries
    templates_google = ["why are term_to_use so"]
    templates_baidu = ["为什么待替换词汇这么", "待替换词汇为什么这么"]

    # DataFrames for suggestions
    df_google = pd.DataFrame(columns=['query', 'suggestion', 'category', 'group', 'completion'])
    df_baidu = pd.DataFrame(columns=['query', 'suggestion', 'category', 'group', 'completion'])

    # Process for Google using English terms
    for category in target_dict_google.keys():
        for template in templates_google:
            for group in target_dict_google[category]:
                query = template.replace("term_to_use", group)
                keywords = query.replace(" ", "+")
                google_suggestions = get_google_suggestions(keywords)

                for suggestion in google_suggestions:
                    completion = suggestion.replace(query, "").strip()
                    new_row = {'query': query, 'suggestion': suggestion, 'category': category, 'group': group, 'completion': completion}
                    df_google = pd.concat([df_google, pd.DataFrame([new_row])], ignore_index=True)

    # Process for Google using English terms
    for category in target_dict_baidu.keys():
        for template in templates_baidu:
            for group in target_dict_baidu[category]:
                query = template.replace("待替换词汇", group)
                keywords = query.replace(" ", "+")
                baidu_suggestions = get_baidu_suggestions(keywords)

                for suggestion in baidu_suggestions:
                    completion = suggestion.replace(query, "").strip()
                    new_row = {'query': query, 'suggestion': suggestion, 'category': category, 'group': group,
                               'completion': completion}
                    df_baidu = pd.concat([df_baidu, pd.DataFrame([new_row])], ignore_index=True)

    # Save results to CSV
    save_df_to_csv(df_google, 'google')
    save_df_to_csv(df_baidu, 'baidu')

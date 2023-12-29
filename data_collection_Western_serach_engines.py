import requests
import json
from fake_useragent import UserAgent  # Ensure you have this library installed
import logging
import pandas as pd


# get data from google
def get_google_suggestions(keyword):
    url = "http://suggestqueries.google.com/complete/search?output=chrome&q=" + keyword + "&hl=en"
    ua = UserAgent()
    headers = {"user-agent": ua.chrome}
    response = requests.get(url, headers=headers, verify=False)
    suggestions = json.loads(response.text)[1]  # Extracting the suggestions list directly

    if not suggestions:
        print("No suggestions:", keyword)  # Debugging statement
    else:
        print("Suggestions for", keyword, ":", suggestions)  # Debugging statement

    return suggestions  # Returning suggestions directly


# get data from duckduckgo
def get_duckduckgo_suggestions(keyword):
    url = 'https://duckduckgo.com/ac/?q=' + keyword + "&hl=en"
    ua = UserAgent()
    headers = {"user-agent": ua.chrome}
    response = requests.get(url, headers=headers)

    try:
        suggestions = [item['phrase'] for item in json.loads(response.text)]
    except json.JSONDecodeError:
        print(f'Failed to parse JSON for keyword: {keyword}')
        return []

    if not suggestions:
        print(f'No suggestions for keyword: {keyword}')  # Debugging statement
    else:
        print(f'Suggestions for {keyword}: {suggestions}')  # Debugging statement

    return suggestions  # Returning suggestions directly


# get data from yahoo
def get_yahoo_suggestions(keyword):
    ua = UserAgent()
    headers = {"user-agent": ua.chrome}
    url = f"http://sugg.search.yahoo.net/sg/?output=chromep&nresults=10&command={keyword}&hl=en"
    response = requests.get(url, headers=headers)

    # Check for a valid response before proceeding
    if response.status_code != 200:
        print(f"Failed to retrieve suggestions for {keyword}: {response.status_code}")
        return []

    print(response.text)  # Add this line to debug the response
    suggestions_data = json.loads(response.text)
    suggestions = [item['key'] for item in suggestions_data['gossip']['results']]
    return suggestions


def get_baidu_suggestions(keyword):
    url = "https://sp0.baidu.com/5a1Fazu8AA54nxGko9WTAnF6hhy/su?wd=" + keyword + "&json=1"
    response = requests.get(url)
    match = re.search(r'{.*}', response.text)
    if match:
        print("Matched string:", match.group())  # Add this line for debugging
        data = json.loads(match.group())
        suggestions = data['s']
        return suggestions
    else:
        return []

data = pd.read_csv("../data/Groups_finnaly.csv")
# translation_dict = data.groupby('Category')['English'].apply(list).to_dict()
translation_dict = data.groupby('Category')['Translation'].apply(list).to_dict()



target_dict = translation_dict
# templates = ["为什么待替换词汇这么", "是什么让待替换词汇这么", "待替换词汇怎么会这么", "为什么待替换词汇总是这么", "为什么所有的待替换词汇都这么"]
# country_templates = ['为什么待替换词汇这么', '是什么让待替换词汇这么', '待替换词汇怎么会这么', '为什么待替换词汇总是这么', '为什么在待替换词汇的所有人都这么']
templates = ["为什么待替换词汇这么","待替换词汇为什么这么"]
# templates = ["why are term_to_use so"]

df_google = pd.DataFrame(columns=['query', 'suggestion', 'category', 'group', 'completion'])  # Added 'completion' column
df_yahoo = pd.DataFrame(columns=['query', 'suggestion', 'category', 'group', 'completion'])  # Added 'completion' column
df_duckduckgo = pd.DataFrame(columns=['query', 'suggestion', 'category', 'group', 'completion'])  # Added 'completion' column
df_baidu = pd.DataFrame(columns=['query', 'suggestion', 'category', 'group', 'completion'])  # Added 'completion' column

for category in target_dict.keys():
    temps = templates
    for group in target_dict[category]:
        for template in temps:  # Use the selected template list
            # query = template.replace("term_to_use", group)
            query = template.replace("待替换词汇", group)
            keywords = query.replace(" ", "+")

            # Fetch suggestions
            google_suggestions = get_google_suggestions(keywords)
            yahoo_suggestions = get_yahoo_suggestions(keywords)
            duckduckgo_suggestions = get_duckduckgo_suggestions(keywords)

            # Add each suggestion to the DataFrame
            for suggestion in google_suggestions:
                completion = suggestion.replace(query, "").strip()  # Remove the original query from the suggestion
                new_row = {'query': query, 'suggestion': suggestion, 'category': category, 'group': group,
                           'completion': completion}
                df_google = pd.concat([df_google, pd.DataFrame([new_row])], ignore_index=True)

            # Add each suggestion to the DataFrame
            for suggestion in duckduckgo_suggestions:
                completion = suggestion.replace(query, "").strip()  # Remove the original query from the suggestion
                new_row = {'query': query, 'suggestion': suggestion, 'category': category, 'group': group,
                           'completion': completion}
                df_duckduckgo = pd.concat([df_duckduckgo, pd.DataFrame([new_row])], ignore_index=True)

            for suggestion in yahoo_suggestions:
                completion = suggestion.replace(query, "").strip()  # Remove the original query from the suggestion
                new_row = {'query': query, 'suggestion': suggestion, 'category': category, 'group': group,
                           'completion': completion}
                df_yahoo = pd.concat([df_yahoo, pd.DataFrame([new_row])], ignore_index=True)

import datetime

# 获取当前日期
current_date = datetime.datetime.now().strftime("%Y-%m-%d")


# 定义一个函数来保存数据框到CSV
def save_df_to_csv(df, search_engine):
    file_name = f"../data/{search_engine}/{search_engine}_Chinese_{current_date}.csv"
    # file_name = f"../data/{search_engine}/{search_engine}_{current_date}.csv"
    df.to_csv(file_name, index=False)


# 保存每个搜索引擎的数据
save_df_to_csv(df_yahoo, 'yahoo')
save_df_to_csv(df_duckduckgo, 'duckduckgo')
save_df_to_csv(df_google, 'google')

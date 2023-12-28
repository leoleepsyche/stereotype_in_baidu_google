import pandas as pd
import requests
import json
import re


data = pd.read_csv('../data/Groups_finnaly.csv')
# 修改的这里
# Grouping the DataFrame by the 'Category' column and collecting translations for each category into lis
# translation_dict = data.groupby('Category')['Translation'].apply(list).to_dict()
translation_dict = data.groupby('Category')['English'].apply(list).to_dict()
# get data from baidu
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

import pandas as pd
import requests
import json
import re
import datetime
target_dict = translation_dict
# templates = ["为什么待替换词汇这么", "是什么让待替换词汇这么", "待替换词汇怎么会这么", "为什么待替换词汇总是这么", "为什么所有的待替换词汇都这么"]
# country_templates = ['为什么待替换词汇这么', '是什么让待替换词汇这么', '待替换词汇怎么会这么', '为什么待替换词汇总是这么', '为什么在待替换词汇的所有人都这么']
# 修改的这里
# templates = ["为什么待替换词汇这么","待替换词汇为什么这么"]
templates = ["why are term_to_use so"]
df = pd.DataFrame(columns=['query', 'suggestion', 'category', 'group', 'completion'])  # Added 'completion' column

for category in target_dict.keys():
    temps = templates
    for group in target_dict[category]:
        for template in temps:  # Use the selected template list
            # 修改这里
            # query = template.replace("待替换词汇", group)
            query = template.replace("term_to_use", group)
            keywords = query.replace(" ", "+")

            # Fetch suggestions
            suggestions = get_baidu_suggestions(keywords)

            # Add each suggestion to the DataFrame
            for suggestion in suggestions:
                completion = suggestion.replace(query, "").strip()  # Remove the original query from the suggestion
                new_row = {'query': query, 'suggestion': suggestion, 'category': category, 'group': group, 'completion': completion}
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

# Define the package name and get the current date
package_name = 'baidu'
# Get the current date
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

#修改的这里

# Set the file name with the package name and the current date
# file_name = f"../data/{package_name}/{package_name}_{current_date}.csv"
file_name = f"../data/{package_name}/{package_name}_English_{current_date}.csv"

# Save the DataFrame to a CSV file
df.to_csv(file_name, index=False)


# Google Dataset Column Descriptions

- **query**: The initial search query. 
- **suggestion**: Google's suggested completion of the query.
- **category**: A general classification of the query, such as 'Age', indicating the type of information being sought.
- **group**: A specific group or subject referenced in the query (e.g., 'boomers').
- **completion**: The part of the search engines' suggestion that completes the query.
- **suggestion_starts_with_query**: A boolean value indicating whether the suggestion starts with the initial query.
- **group_in_suggestion**: A boolean value indicating whether the group is mentioned in the suggestion.
- **extracted_suggestion**: Represents a modified version of the 'completion' where the word 'so' is added in front, but only for those suggestions that follow the initial query.
- **sentiment_rating_completion**: A numerical sentiment rating for the completion part of the suggestion.
- **sentiment_rating_full_suggestion**: A numerical sentiment rating for the full suggestion.

# Baidu Dataset Column Descriptions

- **query**: The initial search query input, in Chinese.
- **suggestion**: Baidu's suggested completion of the query, in Chinese.
- **category**: A general classification of the query, such as 'Age'.
- **group**: The specific group or subject referenced in the query in Chinese (e.g., '儿童' for children).
- **group_English**: The English translation of the group.
- **completion**: The part of the search engines' suggestion that completes  query, in Chinese.
- **completion_English**: The English translation of the completion.
- **suggestion_starts_with_query**: A boolean value indicating whether the suggestion starts with the user's initial query.
- **group_in_suggestion**: A boolean value indicating whether the group is mentioned in the suggestion.
- **extracted_suggestion**: Represents a modified version of the 'completion' where the word 'so' is added in front, but only for those suggestions that follow the initial query in Chinese. 
- **sentiment_rating_completion**: A numerical sentiment rating for the completion part of the suggestion, in Chinese.
- **sentiment_rating_full_suggestion**: A numerical sentiment rating for the full suggestion, in Chinese.

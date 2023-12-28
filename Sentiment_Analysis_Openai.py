import openai
class SharedCounter:
    shared_count = 0

    @classmethod
    def increment(cls):
        cls.shared_count += 1
        return cls.shared_count



def analyze_sentiment(tweet_text):
    # Function to create a chat message
    def create_chat_message(content, role="user"):
        return {"role": role, "content": content}

    # Setup for using the chat model
    sentiment_analysis_message = (
        "Is the sentiment of this text positive, neutral, or negative?\n"
        "Answer only with a number: 1 if positive, 2 if neutral, and 3 if negative.\n"
        "Here is the text:\n"
        f"{tweet_text}"
    )
    messages = [
        create_chat_message("Act as a careful and accurate zero-shot text classifier", role="system"),
        create_chat_message(sentiment_analysis_message)
    ]

    # Chat API call for sentiment rating
    response = openai.ChatCompletion.create(
        # model="gpt-3.5-turbo-1106",
        model = 'gpt-4-1106-preview',
        messages=messages,
        max_tokens=10,
        request_timeout = 600
    )

    # Extracting response for sentiment rating
    sentiment_rating = response.choices[0].message['content'].strip()

    # Ensure the rating is a number and within the expected range
    if sentiment_rating.isdigit() and sentiment_rating in ["1", "2", "3"]:
        sentiment_rating = int(sentiment_rating)
    else:
        sentiment_rating = "Invalid response"

    # Result
    result = {
        "sentiment_rating": sentiment_rating
    }
    # 使用例子
    print(SharedCounter.increment())  # 输出 1
    return result

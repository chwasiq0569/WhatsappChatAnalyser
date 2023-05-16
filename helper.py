import re
from collections import Counter

import pandas as pd
from wordcloud import WordCloud

f = open("G:\DataSciencePortfolioProjects\stop_hinglish.txt", "r")
stop_words = f.read()


def extractURL(message):
    regex_pattern = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    urls = re.findall(regex_pattern, message)
    urls = [x[0] for x in urls]
    return urls


# def remove_stopwords(message):
#     words = []
#     for word in message.lower().split():
#             if word not in stop_words:
#                 words.append(word)
#
#     return words

def fetch_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    num_media = df[df["messages"] == "<Media omitted>\n"].shape[0]

    num_messages = df.shape[0]
    total_words = []
    total_urls = []
    for message in df['messages']:
        words = message.split()
        total_words.extend(words)
        urls = extractURL(message)
        total_urls.extend(urls)

    return num_messages, len(total_words), num_media, len(total_urls)


def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round(df['user'].value_counts() / df.shape[0] * 100, 2).reset_index().rename(
        columns={"index": "user", "user": "percent"})

    return x, df


def create_wordcloud(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    tempdf = df[df['messages'] != "<Media omitted>\n"]
    tempdf = tempdf[tempdf['user'] != "group_notification"]

    def remove_stopwords(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)

        return " ".join(y)

    wc = WordCloud(width=400, height=400, min_font_size=10, background_color='white')
    tempdf['messages'] = tempdf['messages'].apply(remove_stopwords)
    df_wc = wc.generate(tempdf['messages'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    tempdf = df[df['messages'] != "<Media omitted>\n"]
    tempdf = tempdf[tempdf['user'] != "group_notification"]

    words = []
    for message in tempdf['messages']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def monthly_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['messages'].reset_index()
    time_arr = []
    for i in range(timeline.shape[0]):
        time_arr.append(timeline['month'][i] + " - " + str(timeline['year'][i]))

    timeline['time'] = time_arr

    return timeline

def daily_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    daily_timeline_data = df.groupby(['date']).count()['messages'].reset_index()

    return daily_timeline_data

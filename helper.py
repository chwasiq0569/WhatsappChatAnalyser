import re
from wordcloud import WordCloud


def extractURL(message):
    regex_pattern = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    urls = re.findall(regex_pattern, message)
    urls = [x[0] for x in urls]
    return urls


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

    wc = WordCloud(width=400, height=400, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['messages'].str.cat(sep=" "))
    return df_wc

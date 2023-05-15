import re

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
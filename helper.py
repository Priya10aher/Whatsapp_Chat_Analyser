from urlextract import URLExtract # noqa
from wordcloud import WordCloud
extract = URLExtract()
from collections import Counter # noqa
import pandas as pd # noqa
import emoji
import regex


def fetch_stats(selected_user, df):

    if selected_user != 'Overall':

        df = df[df['user'] == selected_user]

    # fetch no. of messages
    num_messages = df.shape[0]

    # fetch total no. of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetch number of links
    links = []

    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)


def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})

    return x, df


def create_wordcloud(selected_user, df):

    f = open('stop_hinglish.txt', 'r')

    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return" ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user, df):

    f = open('stop_hinglish.txt', 'r')

    stop_words = f.read()

    if selected_user != 'Overall':

        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # the goal is to create a string to be put in the function emoji.emoji_list(string)

    words = []
    for messages in df['message']:
        words.extend(messages.split())

    # now we have a list which contains all the words in df['message'] of dataframe
    # now the goal is to convert it into a string

    mystr = ""
    for x in words:
        mystr = mystr + " " + x

    # now we have to put this string into the emoji function

    myemoji = emoji.emoji_list(mystr)

    # myemoji is a list with the following type of elements
    # [{'match_start': 5712, 'match_end': 5714, 'emoji': ''},
    # {'match_start': 6896, 'match_end': 6897, 'emoji': ''},
    # {'match_start': 6897, 'match_end': 6898, 'emoji': ''},
    # {'match_start': 8097, 'match_end': 8098, 'emoji': ''}]

    # now we have to extract each emoji from this type of list

    pre_final_emoji_list = []
    for i in range(len(myemoji)):
        pre_final_emoji_list.extend(myemoji[i]['emoji'])

    # now we have another list which contains all the emojis but it also contains some extra emojis which need to be removed
    # we create two new list, one where removal characters are present and another one where final emojis are.

    emojis_to_be_removed = ['', '']

    final_emoji_list = []
    for items in pre_final_emoji_list:
        if items not in emojis_to_be_removed:
            final_emoji_list.append(items)
    print(final_emoji_list)
    emoji_df = pd.DataFrame(Counter(final_emoji_list).most_common(len(Counter(final_emoji_list))))

    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':

        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


def daily_timeline(selected_user, df):

    if selected_user != 'Overall':

        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user, df):

    if selected_user != 'Overall':

        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):

    if selected_user != 'Overall':

        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user, df):

    if selected_user != 'Overall':

        df = df[df['user'] == selected_user]

    activity_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return activity_heatmap



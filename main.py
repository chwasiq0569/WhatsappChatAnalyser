import helper as helper
import streamlit as st
import matplotlib.pyplot as plt
import helper
import preprocessor

st.sidebar.title('Whatsapp Chat Analyser')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # st.dataframe(df)

    user_list = df['user'].unique().tolist()

    # user_list.remove("group_notification\n")
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show Analysis wrt", user_list)

    if st.sidebar.button('Show Analysis'):
        num_messages, num_words, num_media, total_urls = helper.fetch_stats(selected_user, df)

        st.title('Top Stats')

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(num_words)
        with col3:
            st.header("Media Files")
            st.title(num_media)
        with col4:
            st.header("Total URLs")
            st.title(total_urls)

    st.title("Monthly Timeline")
    timeline = helper.monthly_timeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(timeline['time'], timeline['messages'])
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    st.title("Daily Timeline")
    timeline = helper.daily_timeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(timeline['date'], timeline['messages'])
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    st.title("Activity Map")
    col1, col2 = st.columns(2)

    with col1:
        st.title("Daily Activity Status")
        most_active_days = helper.week_activity_map(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(most_active_days.index, most_active_days.values)
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    with col2:
        st.title("Monthly Activity Status")
        most_active_months = helper.monthly_activity_map(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(most_active_months.index, most_active_months.values)
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


    if selected_user == 'Overall':
        x, new_df = helper.most_busy_users(df)

        fig, ax = plt.subplots()
        ax.bar(x.index, x.values)
        plt.xticks(rotation='vertical')

        st.header("Most Busy Users")
        col1, col2 = st.columns(2)

        with col1:
            st.pyplot(fig)

        with col2:
            st.dataframe(new_df)

    df_wc = helper.create_wordcloud(selected_user, df)
    fig, ax = plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)

    #     most common df

    most_common_df = helper.most_common_words(selected_user, df)

    fig, ax = plt.subplots()

    ax.barh(most_common_df[0], most_common_df[1])
    plt.xticks(rotation='vertical')

    st.dataframe(most_common_df)
    st.pyplot(fig)

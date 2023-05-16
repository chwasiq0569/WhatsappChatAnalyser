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

    st.dataframe(df)

    user_list = df['user'].unique().tolist()

    # user_list.remove("group_notification\n")
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show Analysis wrt", user_list)

    if st.sidebar.button('Show Analysis'):
        num_messages, num_words, num_media, total_urls = helper.fetch_stats(selected_user, df)

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








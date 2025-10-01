import streamlit as st
import praw
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

connection = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
)

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
)


def main():
    st.title("Finance Dashboard")

    st.divider()

    st.sidebar.title("Options")
    options = st.sidebar.selectbox(
        "Select", options=["Pattern", "Reddit", "StockTwits"]
    )

    if options == "Pattern":
        st.text("You just selected pattern page")
        st.image(
            "https://eq-cdn.equiti-me.com/website/images/Artwork_of_different_chart_patterns_for_Chart_.width-800.jpg"
        )

    if options == "Reddit":
        selected_subreddit = st.sidebar.selectbox(
            "Select Subreddit", options=["wallstreetbets", "Daytrading"]
        )

        subreddit = reddit.subreddit(selected_subreddit)

        for submission in subreddit.hot(limit=10):
            with st.container(border=True):
                st.subheader(submission.title)
                st.metric(value=submission.score, label="Score")
                st.link_button(url=submission.url, label="Go to post")

    if options == "StockTwits":
        st.title("Soon...")


if __name__ == "__main__":
    main()

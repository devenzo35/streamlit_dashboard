import streamlit as st
import psycopg2
import psycopg2.extras
import os
import praw  # type: ignore
import pandas as pd
from typing import Union
from dotenv import load_dotenv


load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
)
cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

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
        "Select", ["Chart Viewer", "Trading Journal", "Reddit", "StockTwits"], index=0
    )

    if options == "Chart Viewer":
        symbol = st.text_input(label="Search symbol", max_chars=5, placeholder="AAPL")
        if symbol:
            st.image(f"https://finviz.com/chart.ashx?t={symbol}")

    if options == "Trading Journal":
        query_portfolio = """
            Select s.symbol, SUM(CASE When t.action = 'BUY' then t.quantity else -t.quantity END) as net_quantity,
            (SELECT close FROM prices p Where t.stock_id = p.stock_id LIMIT 1) as last_price
            from trades t
            JOIN stocks s 
            ON s.id = t.stock_id
            GROUP BY s.symbol, t.stock_id
            """

        cursor.execute(query_portfolio)

        counts = cursor.fetchall()

        stock_list: list[dict[str, Union[str, int]]] = [
            {
                "Symbol": c[0],
                "Quantity": c[1],
                "Last_Price": c[2],
            }
            for c in counts
        ]

        pf = pd.DataFrame(stock_list)
        st.write(pf)

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

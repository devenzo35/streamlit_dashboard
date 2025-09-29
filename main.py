import streamlit as st
import pandas as pd
from pandas import DataFrame
from typing import Union


def main():
    st.title("Finance Dashboard")

    st.divider()

    st.sidebar.title("Options")
    options = st.sidebar.selectbox("Select", options=["Pattern", "Tweet", "StockTwits"])

    if options == "Pattern":
        st.text("You just selected pattern page")
        st.image(
            "https://eq-cdn.equiti-me.com/website/images/Artwork_of_different_chart_patterns_for_Chart_.width-800.jpg"
        )

    if options == "Tweet":
        st.text("You just selected Tweet page")
        st.image("https://cdn.mos.cms.futurecdn.net/z3bn6deaxmrjmQHNEkpcZE.jpg")

    if options == "StockTwits":
        st.image("https://upload.wikimedia.org/wikipedia/en/5/58/Stocktiwts.png")


if __name__ == "__main__":
    main()

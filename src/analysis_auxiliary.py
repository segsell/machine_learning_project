"""Auxiliary files for the analysis notebook."""

from typing import List
from typing import Optional
from typing import Union

import matplotlib.dates as dates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from textblob import TextBlob


def plot(
    data: pd.DataFrame,
    date_col: str,
    count_col: str,
    y_label: str = "# of Mentions",
    stock_price_col: Optional[str] = None,
    stock_name: Optional[str] = "GME",
    save_as: Optional[str] = None,
) -> None:
    """Plot count variable and stock price over time."""
    ax = plt.figure(figsize=(17.5, 10)).add_subplot(111)

    plt.xticks(rotation=90)

    ax.set_ylabel(y_label, fontsize=20, color="b")
    ax.tick_params(axis="y", which="major", labelsize=18)
    ax.bar(data[date_col], data[count_col], color="blue", alpha=0.4)

    if isinstance(stock_price_col, str):

        ax2 = ax.twinx()
        ax2.plot(
            data[date_col],
            data[stock_price_col],
            marker="x",
            color="red",
            alpha=0.65,
            linewidth=2,
        )
        ax2.set_ylabel(f"{stock_name} Stock Price", fontsize=20, color="r")
        ax2.tick_params(axis="y", which="major", labelsize=18)

    ax.xaxis.set_major_locator(dates.DayLocator(interval=2))  # every other day
    ax.xaxis.set_major_formatter(dates.DateFormatter("\n%d-%m-%Y"))

    plt.xlim([data[date_col].min(), data[date_col].max()])

    if isinstance(save_as, str):
        plt.savefig(save_as, dpi=300)

    plt.show()


def add_word_counter(
    data: pd.DataFrame,
    text_col: str,
    buzz_words: Union[str, List[str]],
    counter_col: Optional[str] = None,
    case_sensitive: bool = False,
) -> pd.DataFrame:
    """Count mentions of buzz words in reddit submissions."""
    if counter_col is None:
        if isinstance(buzz_words, list):
            counter_col = buzz_words[0]
        else:  # str
            counter_col = buzz_words

    if isinstance(buzz_words, list):
        if len(buzz_words) >= 2:
            buzz_words = "|".join(buzz_words)

    data[counter_col] = np.where(
        data["title"].str.contains(buzz_words, case=case_sensitive), 1, 0
    )
    data_counter = data.copy()
    data_counter = data_counter[data_counter[counter_col] == 1]

    return data_counter


def analyze_sentiment(df: pd.DataFrame, text_col: str) -> pd.DataFrame:
    """Analyze sentiment polarity of posts."""
    for index, _row in df.iterrows():
        body = df.loc[index, text_col]

        if isinstance(body, str):
            blob = TextBlob(body)

            df.loc[index, "sentiment_polarity"] = blob.sentiment.polarity
            df.loc[index, "sentiment_subjectivity"] = blob.sentiment.subjectivity

    return df


def create_date_cols_reddit_data(df: pd.DataFrame, date_col: str) -> pd.DataFrame:
    """Create hourly and daily date columns in stock price data."""
    df = col_to_datetime(df, date_col)

    df["date_hour"] = df[date_col].dt.ceil("H")
    df["date_day"] = df[date_col].dt.floor("D")

    return df


def create_date_cols_stock_data(
    df: pd.DataFrame, date_col: str, stock_name: str, stock_col: str = "symbol"
) -> pd.DataFrame:
    """Create hourly and daily date columns in stock price data."""
    df = df.loc[df[stock_col] == stock_name]
    data = df.copy()

    data["date_day"] = data[date_col].str.replace("T", " ")
    data["date_day"] = data["date_day"].str.replace("Z", "")

    data = col_to_datetime(data, "date_day")
    data["date_day"] = data["date_day"].dt.floor("D")

    data["date_hour"] = data[date_col].str.replace("T", " ")
    data["date_hour"] = data["date_hour"].str.replace("Z", "")

    data = col_to_datetime(data, "date_hour")

    return data


def merge_reddit_and_stock_data(
    reddit_data: pd.DataFrame, stock_data: pd.DataFrame, date_col: str, counter_col: str
) -> pd.DataFrame:
    """Merge reddit and stock price data."""
    # Sum mentions of buzz words within given time period (*date_col*)
    reddit_with_date = pd.merge(
        pd.DataFrame(reddit_data.groupby(date_col)[counter_col].sum()),
        reddit_data[
            [
                date_col,
                "score",
                "upvote_ratio",
                "num_comments",
                "num_crossposts",
                "subreddit_subscribers",
                "author",
                "author_fullname",
                "author_premium",
                "no_follow",
                "all_awardings",
                "total_awards_received",
                "stickied",
                "sentiment_polarity",
                "sentiment_subjectivity",
            ]
        ],
        how="left",
        on=date_col,
    )

    reddit_with_date.reset_index(level=0, inplace=True)
    data_merge = pd.merge(stock_data, reddit_with_date, how="left", on=date_col)

    return data_merge


def col_to_datetime(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """Change format of col from str to pd.datetime."""
    df[col] = pd.to_datetime(df[col])

    return df

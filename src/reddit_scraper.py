"""Reddit scraper."""
import time
from datetime import datetime
from typing import Any
from typing import Dict
from typing import Optional

import pandas as pd
import requests


JsonDict = Dict[str, Any]


def scrape_reddit_data(
    subreddit: str,
    url: str,
    before_date: str,
    after_date: str,
    save_as: Optional[str] = None,
) -> pd.DataFrame:
    """Scrape all submissions (or comments) of a particular ``subreddit``.

    The pushshift API is used to retrieve the data, where all submissions
    (or comments) between ``after_date`` and ``before_date`` are scraped.
    ``url`` determines whether to scrape submissions or comments.

    The downloaded data may be saved to disc as a csv file.

    Arguments:
        subreddit: Name of the subreddit.
        url: URL to the pushshift API.
        before_date: Date in UNIX time (https://www.unixtimestamp.com/index.php)
            prior to which the submissions or comments are requestd.
        after_date: Date in UNIX time marking the start of the search interval.
        save_as: Path to save data (csv format).

    Returns:
        data_all: DataFrame containing all reddit submissions (or comments) of the
        provided time frame.

    """
    df_list = []
    filtered_columns = [
        "subreddit",
        "subreddit_id",
        "subreddit_subscribers",
        "title",
        "is_original_data",
        "created_utc",
        "retrieved_on",
        "score",
        "upvote_ratio",
        "num_comments",
        "num_crossposts",
        "cross_postable",
        "domain",
        "full_link",
        "author",
        "author_fullname",
        "author_premium",
        "no_follow",
        "all_awardings",
        "total_awards_received",
        "is_video",
        "id",
        "link_id",
        "url",
        "permalink",
    ]

    while after_date < before_date:
        print(
            "Collect entries before: "
            f"{datetime.utcfromtimestamp(before_date).strftime('%Y-%m-%d %H:%M:%S')}"
        )

        res = request_json(subreddit, url, before_date)
        time.sleep(3)

        df = pd.DataFrame(res.json()["data"])
        df = df.reindex(columns=filtered_columns)

        df_list.append(df)
        before_date = df.created_utc.min()

    data_all = pd.concat(df_list, axis=0)
    data = process_scraped_df(data_all)

    if isinstance(save_as, str):
        save_as = save_as if save_as.endswith(".csv") else save_as + ".csv"
        data.to_csv(save_as, index=False)

    return data_all


def request_json(subreddit: str, url: str, before_date: str) -> JsonDict:
    """Retrieve data from the pushshift API.

    The request object is a json file and contains
    the first 500 submissions or comments prior to ``before_date``.

    Arguments:
        subreddit: Name of the subreddit.
        url: URL to the pushshift API.
        before_date: Date in UNIX time (https://www.unixtimestamp.com/index.php)
            prior to which the submissions or comments are requestd.

    Returns:
        Json dictionary containing requested data from the pushshift API.

    """
    while True:
        try:
            req = requests.get(
                url,
                params={
                    "subreddit": subreddit,
                    "size": 500,
                    "before": before_date,
                },
            )
            if req.status_code != 200:
                print("error code", req.status_code)
                time.sleep(5)
                continue
            else:
                break
        except Exception as ex:
            print(ex)
            time.sleep(5)
            continue

    return req


def process_scraped_df(data: pd.DataFrame) -> pd.DataFrame:
    """Sort scraped reddit data and select columns.

    Arguments:
        data: Raw reddit data scraped from the pushshift API.

    Returns:
        outdata: Data sorted by "date". A subset of relevant columns is kept.

    """
    col_list = [
        "subreddit",
        "subreddit_id",
        "subreddit_subscribers",
        "title",
        "is_original_data",
        "date",
        "created_utc",
        "retrieved_on",
        "score",
        "upvote_ratio",
        "num_comments",
        "num_crossposts",
        "cross_postable",
        "domain",
        "full_link",
        "author",
        "author_fullname",
        "author_premium",
        "no_follow",
        "all_awardings",
        "total_awards_received",
        "is_video",
        "id",
        "link_id",
        "url",
        "permalink",
    ]

    data["date"] = pd.to_datetime(data["created_utc"], unit="s")
    data.sort_values(by=["date"], inplace=True)

    outdata = data.reset_index(drop=True)
    outdata = outdata[col_list]

    return outdata


if __name__ == "__main__":
    subreddit = "wallstreetbets"
    url_submissions = "https://api.pushshift.io/reddit/search/submission"
    before = int(datetime(2021, 2, 21, 0, 0).timestamp())  # Feb 28th 2021
    after = int(datetime(2021, 1, 31, 0, 0).timestamp())  # Sep 1st 2020
    data = scrape_reddit_data(
        subreddit,
        url_submissions,
        before,
        after,
        save_as="data/wsb_sep_01_feb_28_raw.csv",
    )

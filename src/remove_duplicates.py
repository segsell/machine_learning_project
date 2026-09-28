"""Remove duplicates from reddit data."""

from typing import Optional

import pandas as pd


def remove_duplicates(
    data: pd.DataFrame, save_as: Optional[str] = None
) -> pd.DataFrame:
    """Remove duplicate rows from reddit data.

    Observations qualify as duplicate if a given ("title", "author") pair
    appears multiple times. In such a case, their "score" and "num_comments"
    are added up and only the first observation (by "date") is kept.

    Arguments:
        data: Raw reddit data.
        save_as: Path to save cleaned data.

    Returns:
        data_clean: Clean data without duplicates.

    """
    cols = [
        "title",
        "stickied",
        "date",
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
        "is_video",
        "id",
    ]
    data = data[cols]

    duplicates = data[
        data[["title", "author"]].duplicated(keep=False) == True
    ].sort_values(["title", "num_comments"], ascending=False)
    data_dups_dropped = data.drop(duplicates.index)

    sum_score = duplicates.groupby(["author", "title"])["score"].sum().to_frame()
    sum_comments = (
        duplicates.groupby(["author", "title"])["num_comments"].sum().to_frame()
    )
    sum_awards = (
        duplicates.groupby(["author", "title"])["total_awards_received"]
        .sum()
        .to_frame()
    )

    data_sum_score_comments_awards = duplicates.sort_values(
        ["author", "date"], ascending=True
    ).drop_duplicates(["title", "author"], keep="first")
    data_sum_score_comments_awards["score"] = list(sum_score["score"])
    data_sum_score_comments_awards["num_comments"] = list(sum_comments["num_comments"])
    data_sum_score_comments_awards["total_awards_received"] = list(
        sum_awards["total_awards_received"]
    )

    data_clean = pd.concat([data_dups_dropped, data_sum_score_comments_awards])
    data_clean = data_clean.sort_values(["date"])
    data_clean = data_clean.reset_index(drop=True)

    if isinstance(save_as, str):
        save_as = save_as if save_as.endswith(".csv") else save_as + ".csv"
        data_clean.to_csv(save_as, index=False)

    return data_clean


if __name__ == "__main__":
    data = pd.read_csv("data/wsb_sep_01_feb_28_raw.csv")
    data_clean = remove_duplicates(data, save_as="data/wsb_sep_01_feb_28.csv")

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
        "date",
        "score",
        "num_comments",
        "num_crossposts",
        "total_awards_received",
        "author",
    ]
    data = data[cols]

    duplicates = data[
        data[["title", "author"]].duplicated(keep=False) == True
    ].sort_values(["title", "num_comments"], ascending=False)
    data_no_dup = data.drop(duplicates.index)

    sum_score = duplicates.groupby(["author", "title"])["score"].sum().to_frame()
    sum_comments = (
        duplicates.groupby(["author", "title"])["num_comments"].sum().to_frame()
    )
    data_sum_score_comments = duplicates.sort_values(
        ["author", "date"], ascending=True
    ).drop_duplicates(["title", "author"], keep="first")
    data_sum_score_comments["score"] = list(sum_score["score"])
    data_sum_score_comments["num_comments"] = list(sum_comments["num_comments"])

    data_clean = pd.concat([data_no_dup, data_sum_score_comments])
    data_clean = data_clean.sort_values(["date"])
    data_clean = data_clean.reset_index(drop=True)

    if isinstance(save_as, str):
        save_as = save_as if save_as.endswith(".csv") else save_as + ".csv"
        data_clean.to_csv(save_as, index=False)

    return data_clean


if __name__ == "__main__":
    data = pd.read_csv("data/wsb_jan_01_feb_05_raw.csv")
    data_clean = remove_duplicates(data, save_as="data/wsb_jan_01_feb_05_clean.csv")

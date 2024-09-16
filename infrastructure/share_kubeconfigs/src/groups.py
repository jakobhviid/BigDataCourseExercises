from pathlib import Path

import pandas as pd

from .students import STUDENT_MAIL_PATTERN

GROUP_PATTERN: str = "group-"


def apply_group_pattern(x: str, n_fill: int = 2) -> str:
    return f"{GROUP_PATTERN}{str(x).zfill(n_fill)}"


def parse_groups_from_form(filename: Path, col_id: str = "Id") -> pd.DataFrame:
    form_col_pattern: str = "SDU student mail"

    df = pd.read_csv(filename, sep=";")
    df = df[[col_id] + [col for col in df.columns if col.startswith(form_col_pattern)]]

    df = df.melt(id_vars=[col_id])[[col_id, "value"]]
    df.dropna(inplace=True)

    df["value"] = df["value"].apply(lambda x: x.replace(STUDENT_MAIL_PATTERN, ""))
    df[col_id] = df[col_id].apply(lambda x: apply_group_pattern(x))

    df.sort_values(by=col_id, inplace=True)

    return df

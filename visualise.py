import sys
import os

import pandas as pd

import colorcet as cc
import seaborn as sns

import matplotlib.pyplot as plt


if __name__ == "__main__":
    filename = sys.argv[1]

    description = os.path.basename(filename)
    description = os.path.splitext(description)[0]

    condition = "Condition in 2022"
    county = "County"

    df = pd.read_csv(filename)
    df = df.rename(columns={"Zustand 2022": condition, "LAND": county})

    df = df.replace("mangelhaft", "deficient")
    df = df.replace("schlecht", "poor")
    df = df.replace("einschränkend", "restrictive")

    order = ["poor", "deficient", "restrictive"]

    # Not all data files contain all counties. This ensures a consistent
    # ordering.
    hue_order = [
        "BB",
        "BE",
        "BW",
        "BY",
        "HB",
        "HE",
        "HH",
        "MV",
        "NI",
        "NW",
        "RP",
        "SH",
        "SL",
        "SN",
        "ST",
        "TH",
    ]

    print(df)

    sns.catplot(df, x=condition, order=order, kind="count")
    plt.title(description)
    plt.tight_layout()

    plt.savefig("figures/" + description.lower() + ".png")

    sns.catplot(
        df,
        x=condition,
        order=order,
        hue=county,
        hue_order=hue_order,
        kind="count",
        palette=sns.color_palette(cc.glasbey_light, n_colors=16)
    )

    plt.title(description + " (by county)")
    plt.tight_layout()

    plt.savefig("figures/" + description.lower() + "_by_county" + ".png")

    plt.show()

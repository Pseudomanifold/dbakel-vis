import sys
import os

import pandas as pd
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
    hue_order = sorted(df[county].unique())

    print(df)

    sns.color_palette("Set2")

    sns.catplot(df, x=condition, order=order, kind="count")
    plt.title(description)
    plt.tight_layout()

    sns.catplot(
        df,
        x=condition,
        order=order,
        hue=county,
        hue_order=hue_order,
        kind="count",
        palette="Set2",
    )

    plt.title(description + " (by county)")
    plt.tight_layout()

    plt.show()

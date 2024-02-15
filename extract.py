import fitz
import pandas as pd


# Auxiliary function for creating a data frame from a set of rows. This
# is required because I do not want to repeat the creation step for the
# last table in the file.
def _make_data_frame(rows):
    df = pd.DataFrame.from_records(rows)
    df = df.rename(columns=df.iloc[0])
    df = df.drop(df.index[0])

    return df


if __name__ == "__main__":
    doc = fitz.open("raw/2010284.pdf")

    current_table = []
    all_tables = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        tabs = page.find_tables()

        for tab in tabs:
            tab = tab.extract()

            # Start a new table; the first column always signifies the
            # county of the respective object.
            if tab[0][0] == "LAND":
                if len(current_table) > 0:
                    print(f"Finished table on page {page_num}")

                    all_tables.append(_make_data_frame(current_table))
                    current_table = []

            for row in tab:
                current_table.append(row)

    # Finish the last table in the file (we can only do this _after_
    # parsing all lines).
    if len(current_table) > 0:
        all_tables.append(_make_data_frame(current_table))

    descriptions = ["Tracks", "Bridges", "Switches", "Crossings", "Structures"]

    # Basic sanity check; if this goes wrong, you have the wrong file
    # somehow...
    assert len(all_tables) == len(descriptions)

    for table, description in zip(all_tables, descriptions):
        table.to_csv(f"tables/{description}.csv", index=False)

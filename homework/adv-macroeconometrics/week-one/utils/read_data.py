import pandas as pd

def format_dates(series):
    qs = series.apply(
        lambda q: "-Q".join([str(int(n)) for n in str(q).split(":")])
    )
    
    return pd.PeriodIndex(qs.values, freq="Q")



def read_data(name, f = ""):


    if 'csv' in name:
        df = pd.read_csv(name)
    elif 'xls' in name:
        df = pd.read_excel(name)

    else:
        raise ValueError("File type not understood")

    df = df.dropna(axis = 1).rename(columns={"Unnamed: 0": "t"})

    df["t"] = format_dates(df["t"])

    f = f if len(f) > 0 else df["t"][0]

    return df.set_index("t")[f:]
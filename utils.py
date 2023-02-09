import pandas as pd

def getStandartRt(df, sd=3):
    mean_rt = df.rt.mean()
    std_rt = df.rt.std()
    standard_df = df[(df.rt > (mean_rt - (sd * std_rt)))
                          & (df.rt < (mean_rt + (sd * std_rt)))]
    return standard_df

def get_df_without_outliers(df, cols=[], sds = 2.5):
    for col in cols:
        mean = df[col].mean()
        sd = df[col].std()
        df = df[(df[col] > mean - sds * sd) & (df[col] < mean + sds * sd)]
    return df

def fix_numeric_columns(df, columns=[]):
    for col in columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df
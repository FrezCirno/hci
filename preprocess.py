import pandas as pd

df = pd.read_csv("dataset/google-play-store-apps/googleplaystore.csv")


def parse_number(s: str):
    s = s.replace(',', '')

    unit = s[-1]
    try:
        if unit == 'M':
            return int(float(s[:-1]) * 1000000)
        elif unit == 'k':
            return int(float(s[:-1]) * 1000)
        return int(s)
    except:
        return 0


df['Size'] = df['Size'].apply(parse_number)
df['Installs'] = df['Installs'].apply(lambda s: int(s.replace(",", '').rstrip("+")))
df['Price'] = df['Price'].apply(lambda s: float(s.lstrip('$')))
df['Rating'] = df['Rating'].fillna(0)
df.dropna(inplace=True)
df.info()

# for col in df.columns:
#     pd.DataFrame(df[col].unique()).to_csv('dataset/google-play-store-apps/'+col+'.csv')

df.to_csv("dataset/google-play-store-apps/googleplaystore_pre.csv", index=None)

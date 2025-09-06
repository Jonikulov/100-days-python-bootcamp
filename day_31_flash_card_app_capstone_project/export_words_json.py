import pandas as pd
import json

CSV_FILE_PATH = "./data/turkish-english-words.csv"
df = pd.read_csv(CSV_FILE_PATH)
df = df.sample(frac=1)  # random shuffle the dataframe

# words = {
#     "LEARN":[
#         {"Turkish": tw, "English": ew} for tw, ew in zip(df["Turkish"].to_list(), df["English"].to_list())
#     ],
#     "KNOW":[],
# }

words = {
    "LEARN": df.to_dict(orient="records"),
    "KNOW":[],
}

print(words.keys())

with open("./data/turkish-english-words.json", "w", encoding="utf-8") as file:
    json.dump(words, file, indent=4, ensure_ascii=False)

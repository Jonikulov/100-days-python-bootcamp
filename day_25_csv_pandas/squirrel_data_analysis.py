import pandas as pd

file_name = "2018_Central_Park_Squirrel_Census_-_Squirrel_Data.csv"
df = pd.read_csv(file_name)
# df.info()
# print(df.head())

# Create squirrel count csv data (fur color, count)
col = "Primary Fur Color"
col_value_counts = df[col].value_counts()
print(col_value_counts)
col_value_counts.to_csv("squirrel_count.csv")

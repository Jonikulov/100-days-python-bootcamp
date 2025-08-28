"""Day 25. CSV, Pandas"""

# data_lines = []

# for line in open("weather_data.csv"):
#     data_lines.append(line.strip())

# print(data_lines)

###############################################################################

# import csv

# with open("weather_data.csv") as file:
#     data = csv.reader(file)
#     temperatures = []
#     for row in list(data)[1:]:
#         temperatures.append(int(row[1]))

# print(temperatures)

###############################################################################

import pandas as pd

df = pd.read_csv("weather_data.csv")
# df.info()

# temps = df["temp"].to_list()
# avg_temp = sum(temps) / len(temps)
# print("Avg Temp:", round(avg_temp, 2))

print("Mean Temp:", df["temp"].mean())
print("Max Temp:", df["temp"].max())
# Get data in row
# print(df.iloc[[1], :])
print(df.loc[[df.temp.idxmax()]])

monday = df[df["day"]=="Monday"]
mon_temp = monday.temp[0]
print(f"Monday Temp: {mon_temp} C = {mon_temp * 9/5 + 32} F")

# Create a DataFrame from scratch
data_dict = {
    "students": ["Amy", "James", "Angela"],
    "scores": [76, 56, 65]
}
data = pd.DataFrame(data_dict)
data.to_csv("new_data.csv")

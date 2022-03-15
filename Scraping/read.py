import pandas as pd

### Loop the data lines
with open("items.txt", 'r', encoding="utf8") as temp_f:
    # get No of columns in each line
    col_count = [ len(l.split(",")) for l in temp_f.readlines() ]

### Generate column names  (names will be 0, 1, 2, ..., maximum columns - 1)
column_names = [i for i in range(0, max(col_count))]

### Read csv
df = pd.read_csv("items.txt", header=None, delimiter=",", names=column_names)
df.to_excel("items.xlsx")

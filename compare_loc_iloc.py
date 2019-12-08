import pandas as pd

a = pd.DataFrame({"a":[1,2,3],"b":[4,5,6]})
print(a.loc[1,"a"])
print(a.iloc[1,0])

import pandas as pd

df = pd.DataFrame({'a':[1,2,1], 'b':[1,1,1]})
print(df['a'] == 1)
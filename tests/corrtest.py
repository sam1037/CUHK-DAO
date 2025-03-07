# import pandas
import pandas as pd
 
# obtaining the data
data = {'A': [45, 37, 42],
        'B': [38, 31, 26],
        'C': [10, 15, 17]
        }
# creation of DataFrame
df = pd.DataFrame(data)
 
# creation of correlation matrix
corrM = df.corr()
 
corrM
import pandas as pd
import numpy as np

def readCSV(dst):
    df = pd.read_csv(dst)
    #print(df)
    df = np.array(df)
    num = len(df)
    return num, df


import pandas as pd
def getCSV(kwd):
    df = pd.read_csv('./database/database.csv')
    #print(df)
    line1 = df[df.ID.isin([kwd])]
    #print(line1)
    if (len(line1) == 0):
         return False, str(df.iloc[0]["ID"]), str(df.iloc[0]["Time"]), str(df.iloc[0]["Status"])
    else:
         #print(type("-1"), type(str(line1["ID"].values)))
         return True, str(line1.iloc[0]["ID"]), str(line1.iloc[0]["Time"]), str(line1.iloc[0]["Status"])

if __name__ =='__main__':
    find, s1, s2, s3 = getCSV(1)
    # print(len(s1))
    # print()
    # print(s1, s2, s3)
    print("ID: " + s1 + "\tTime: " + s2 + "\tStatus: " + s3)

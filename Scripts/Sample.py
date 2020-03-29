import os
path=input("Enter your directory path: ")
df_1=os.listdir(path)
print(df_1)
p1=df_1[0]
p2=os.path.join(path,df_1[1])
print(p2)



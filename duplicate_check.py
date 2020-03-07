import pandas as pd
file_name =input("Enter Source file Name") 
df = pd.read_csv(file_name,sep="|", quotechar='"', decimal=",",low_memory=False,encoding='utf-8')
#print(df.shape)

mask = df.duplicated()

print('No.of Rows in file: ',df.shape[0])

if (df[mask].shape[0])>0:
  print('Duplicates Found : Yes')
  #print('\n')
  print('No.of Duplicate Records in file: ',df[mask].shape[0])
else:
  print('Duplicates Found : No')


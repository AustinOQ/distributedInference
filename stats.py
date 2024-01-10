data=open("OneDevice0-3NoSplit.txt","r").readlines()
sum=0
for i in data:
    sum+=float(i)
print(sum/len(data))
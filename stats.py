data=open(input("Enter relative file path:"),"r").readlines()
sum=0
for i in data:
    sum+=float(i)
print(sum/len(data))
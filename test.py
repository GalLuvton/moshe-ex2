from random import randint

filename = "C:\\Users\\dell\\Desktop\\shittest.csv"
with open(filename, 'wb') as f:
    for i in range(20):
        for j in range(20):
            if randint(0, 9) > 5:
                f.write(str(i+1) + "\t" + str(j+1) + "\t" + str(randint(1, 5)) + "\t1\n")

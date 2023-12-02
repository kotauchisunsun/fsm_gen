for i in range(2,100):
    for j in reversed(range(1,i)):
        if j == 1:
            print(i)
        if i%j==0:
            break
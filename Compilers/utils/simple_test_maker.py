test = ["(1+1)*3","(1+/*A */1)*10","(1+1)*(2+2)","(10*(9*9))","(((1+1)))","1+(1","1+1)","(1+(1)","(1-(1)","-1","--2","- -2","--2+40","40--2","44---2","40+-+-2","40+++++++++2"]
sol = ["6","20","8","810","2","Error","Error","Error","Error","-1","2","2","42","42","42","42","42"]

if (len(test) != len(sol)):
    raise Exception("len Sol != test")

init = 29
counter = init
while counter < (len(test) +init):
    print(counter)

    new_test = "new-test/teste{!s}.txt".format(counter)
    with open(new_test, 'w') as file:
        file.write(test[counter - init])

    new_sol = "new-test/sol{!s}.txt".format(counter)
    with open(new_sol, 'w') as file:
        file.write(sol[counter - init])

    counter+=1


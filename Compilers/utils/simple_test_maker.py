test = ["/* A /* 1 */ 2","/* A */ 1 /* A */","1 + /* 2 */ 3","/* A 1","1 /* A","1 + /* A */ */"]
sol = ["2","1","4","Error","Error","Error"]

if (len(test) != len(sol)):
    raise Exception("len Sol != test")

init = 24
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


test = ["1*1","1/1","32*985","3168/99","2+5*4","2*4/2","0/1","8  * 9 / 2","4//2","3**3","8//4**2"]
sol = ["1","1","31520","32","22","4","0","36","Error","Error","Error"]

if (len(test) != len(sol)):
    raise Exception("len Sol != test")

init = 12
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


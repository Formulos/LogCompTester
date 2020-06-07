a1= \
"""<?php
{
    function hello() {
        echo 42;
        }
    hello();
    
}
?>"""
s1 = "42"

a2= \
"""<?php
{
    function recursivo($x) {
        if ($x > 0){
            $x = $x - 1;
            $x = recursivo($x);
            }
            return $x;
        }
    $x = 10;
    $x = recursivo($x);
    echo $x;
    
}
?>"""
s2 = "0"

a3= \
"""<?php
{
    function independence($x) {
        $x = 42;
        return $x;
        }
    $x = 10;
    independence($x);
    echo $x;
    
}
?>"""
s3 = "10"

a4= \
"""<?php
{
    function soma($x, $y) {
        function echoes($b) {
            echo $b;
            }
        $a = $x + $y;
        echoes($a);
        return $a;
        }
    $a = 3;
    $b = soma($a, 4);
    echo $b;
    echoes($a);
    
}
?>"""
s4="""7
7
3"""

a5= \
"""<?php
{
    function soma($x, $y) {
        function echoes($b) {
            echo $b;
            }
        $a = $x + $y;
        echoes($a);
        return $a;
        }
    $a = 3;
    $b = soma($a, 4);
    echo $b;
    echoes($a);
    $c = soma($b, $a); 
    
}
?>"""
s5="""Error"""

a6= \
"""<?php
{
    function soma($x, $y) {
        function echoes($b) {
            echo $b;
            }
        $a = $x + $y;
        echoes($a);
        return $a;
        }
    $a = 3;
    echoes($a); /* ERROR: Soma nunca chamada = echoes não declarado */  
}
?>"""
s6="""Error"""

a7= \
"""<?php
{
    function muitos($x, $y) {
        return 1;
        }
    $a = 3;
    muitos($a,3,3);
}
?>"""
s7="""Error"""

a8= \
"""<?php
{
    function poucos($x, $y) {
        return 1;
        }
    $a = 3;
    poucos($a);
}
?>"""
s8="""Error"""

a9= \
"""<?php
{
    function direto($x) {
        return $x;
        }
    $a = direto(42);
    echo $a;
}
?>"""
s9="""42"""

test = [a1,a3,a4,a5,a6,a8,a9]
sol = [s1,s3,s4,s5,s6,s8,s9]
inp = []

if (len(test) != len(sol)):
    raise Exception("len Sol != test")

init = 1
counter = init
while counter < (len(test) +init):
    print(counter)

    new_test = "new-test/teste{!s}.php".format(counter)
    with open(new_test, 'w') as file:
        file.write(test[counter - init])

    #new_sol = "new-test/sol{!s}.txt".format(counter)
    #with open(new_sol, 'w') as file:
    #    file.write(sol[counter - init])

    #new_input = "new-test/inputs/input{!s}.txt".format(counter)
    #with open(new_input, 'w') as file:
    #    file.write(inp[counter - init])

    counter+=1


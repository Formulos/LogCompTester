a1= \
"""<?php\n{
    if (true){
        echo 1;
    }
}
?>"""
s1="""1"""

a2= \
"""<?php\n{
    if (true or false){
        echo 1;
    }
}
?>"""
s2="""1"""

a3= \
"""<?php\n{
    if (true and (1==1)){
        echo 1;
    }
}
?>"""
s3="""1"""

a4= \
"""<?php\n{
    if (!(false)){
        echo 1;
    }
}
?>"""
s4="""1"""

a5= \
"""<?php\n{
    if (true and (!(1==1))){
        echo 1;
    }
    else{
        echo 2;
    }
}
?>"""
s5="""2"""

a6= \
"""<?php\n{
  $x = true;
  if ($x){
    echo 42;
  }
}
?>"""
s6="""42"""

a7= \
"""<?php\n{
  $x = true;
  if ($x){
    echo 42;
  }
}
?>"""
s7="""42"""

a8= \
"""<?php\n{   
    if (((true) or (TrUe) OR (TRUE)) oR ((false) AND (False) AnD (FALSE))){
        echo 42;
    }
}
?>"""
s8="""42"""

a9= \
"""<?php\n{
    $a = true;
    $b = TrUe;
    $c = TRUE;
    $d = false;
    $e = False;
    $f = FALSE;
    if ((($a) or ($b) OR ($c)) oR (($d) AND ($e) AnD ($f))){
        echo 42;
    }
}
?>"""
s9="""42"""

a10= \
"""<?php\n{
    $y = true+1;
    echo $y;
}
?>"""
s10="""2"""

a11= \
"""<?php\n{
    $y = false+1;
    echo $y;
}
?>"""
s11="""1"""

a12= \
"""<?php\n{
  if(1){
    echo 42;
  }
}
?>"""
s12="""42"""

a13= \
"""<?php\n{
  if(2){
    echo 42;
  }
}
?>"""
s13="""42"""

a14= \
"""<?php\n{
  if(2 or false){
    echo 42;
  }
}
?>"""
s14="""42"""

a15= \
"""<?php\n{
    if(0 or false){
        echo 1;
    }
    else{
        echo 42;
    }
}
?>"""
s15="""42"""

a16= \
"""<?php\n{
    if(0 or false){
        echo 1;
    }
    else{
        echo 42;
    }
}
?>"""
s16="""42"""

a17= \
"""<?php\n{
    $a = "hello";
    echo $a;
}
?>"""
s17="""hello"""

a18= \
"""<?php\n{
    $a = "hello" . " world";
    echo $a;
}
?>"""
s18="""hello world"""

a19= \
"""<?php\n{
    $b = 57;
    $a = "esse é o teste " . $b . " eu acho";
    echo $a;
}
?>"""
s19="""esse é o teste 57 eu acho"""

a20= \
"""<?php\n{
    $a = 1 . true . "a";
    echo $a;
}
?>"""
s20="""11a"""

a21= \
"""<?php\n{
    $a = 1 + "a";
}
?>"""
s21="""Error"""

a22= \
"""<?php\n{
    if("a"){
        echo 1
    }
}
?>"""
s22="""Error"""

a23= \
"""
<?php
$a = 1 + "a";
?>

"""
s23="""Error"""

a24= \
"""<?php\n{
    if("a"){
        echo 1
    }
}
"""
s24="""Error"""

a25= \
"""<?php\n{
    $x = readline()+1;
    echo $x;
}?>
"""
s25="""Error"""




test = [a1,a2,a3,s4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16,a17,a18,a19,a20,a21,a22,a23,a24,a25]
sol = [s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,s14,s15,s16,s17,s18,s19,s20,s21,s22,s23,s24,s25]
inp = []

if (len(test) != len(sol)):
    raise Exception("len Sol != test")

init = 39
counter = init
while counter < (len(test) +init):
    print(counter)

    new_test = "new-test/teste{!s}.php".format(counter)
    with open(new_test, 'w') as file:
        file.write(test[counter - init])

    new_sol = "new-test/sol{!s}.txt".format(counter)
    with open(new_sol, 'w') as file:
        file.write(sol[counter - init])

    #new_input = "new-test/inputs/input{!s}.txt".format(counter)
    #with open(new_input, 'w') as file:
    #    file.write(inp[counter - init])

    counter+=1


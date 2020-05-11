a1= \
"""{
    if (true){
        echo 1;
    }
}
"""
s1="""1"""

a2= \
"""{
    if (true or false){
        echo 1;
    }
}
"""
s2="""1"""

a3= \
"""{
    if (true and (1==1)){
        echo 1;
    }
}
"""
s3="""1"""

a4= \
"""{
    if (!(false)){
        echo 1;
    }
}
"""
s4="""1"""

a5= \
"""{
    if (true and (!(1==1))){
        echo 1;
    }
    else{
        echo 2;
    }
}
"""
s5="""2"""

a6= \
"""{
  $x = true;
  if ($x){
    echo 42;
  }
}
"""
s6="""42"""

a7= \
"""{
  $x = true;
  if ($x){
    echo 42;
  }
}
"""
s7="""42"""

a8= \
"""{   
    if (((true) or (TrUe) OR (TRUE)) oR ((false) AND (False) AnD (FALSE))){
        echo 42;
    }
}
"""
s8="""42"""

a9= \
"""{
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
"""
s9="""42"""

a10= \
"""{
    $y = true+1;
    echo $y;
}
"""
s10="""2"""

a11= \
"""{
    $y = false+1;
    echo $y;
}
"""
s11="""1"""

a12= \
"""{
  if(1){
    echo 42;
  }
}
"""
s12="""42"""

a13= \
"""{
  if(2){
    echo 42;
  }
}
"""
s13="""42"""

a14= \
"""{
  if(2 or false){
    echo 42;
  }
}
"""
s14="""42"""

a15= \
"""{
    if(0 or false){
        echo 1;
    }
    else{
        echo 42;
    }
}
"""
s15="""42"""

a16= \
"""{
    if(0 or false){
        echo 1;
    }
    else{
        echo 42;
    }
}
"""
s16="""42"""

a17= \
"""{
    $a = "hello";
    echo $a;
}
"""
s17="""hello"""

a18= \
"""{
    $a = "hello" . " world";
    echo $a;
}
"""
s18="""hello world"""

a19= \
"""{
    $b = 57;
    $a = "esse é o teste " . $b . " eu acho";
    echo $a;
}
"""
s19="""esse é o teste 57 eu acho"""

a20= \
"""{
    $a = 1 . true . "a";
    echo $a;
}
"""
s20="""11a"""

a21= \
"""{
    $a = 1 + "a";
}
"""
s21="""Error"""

a22= \
"""{
    $a = 1 + "a";
}
"""
s22="""Error"""

a23= \
"""{
    $a = 1 + "a";
}
"""
s23="""Error"""

a24= \
"""{
    $a = 1 + "a";
}
"""
s24="""Error"""




test = [a1,a2,a3,s4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16,a17,a18,a19,a20,a21,a22,a23,a24]
sol = [s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,s14,s15,s16,s17,s18,s19,s20,s21,s22,s23,s24]
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


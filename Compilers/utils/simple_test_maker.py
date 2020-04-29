a0= \
"""
{
    echo "hello";
}
"""
a= \
"""
{

    if (10 < 20) {
        echo "hello!";
    }
}
"""
b= \
"""
{
    
    if (30 < 20) {
    echo "hello!";
    }
    else{
        echo "hello2!";
    }
}
"""
c= \
"""
{
    else{
        echo "hello3!";
    }
}
"""
c= \
"""
{
    else{
        echo "hello2!";
    }
}
"""
d= \
"""
{
    if True {
        echo "hello";
    }
}
"""
e= \
"""
{
    if True or False{
        echo "hello?";
    }
}
"""
f=\
"""
{
    $f = True;
    if ($f){
        echo "hello???";
    }
}
"""
g=\
"""
{
    if (True and false){
        echo "se isso foi imprimido algo deu errado";
    }
    else{
        echo "tudo certo";
    }
}
"""
h=\
"""
{
    if (True or false){
        echo "deu certo";
    }
    else{
        echo "tudo errado";
    }
}
"""
j=\
"""
{
    if (not False) {
        echo "certo2";
    }
    else{
        echo "tudo errado";
    }
}
"""
k=\
"""
{
    if (not ((True or False) and False)){
        echo "certo3";
    }
}
"""
m=\
"""
{   
    $a = 0;
    while ($a < 3){
        $a = $a +1;
        echo $a;
    }
}
"""
ms=\
"""1
2
3"""

n=\
"""
{   
    $a = 0;
    while ($a <= 3){
        $a = $a +1;
        echo $a;
    }
}
"""
ns=\
"""1
2
3
4"""
o=\
"""
{   
    $a = 0;
    $b = True;
    while (($a < 99999) and $b){
        $a = $a +1;
        echo $a;
        if ($a == 5){
            $b = False;
        }
    }
    echo $a;
}
"""
os=\
"""1
2
3
5
5"""

p=\
"""
{   
    $a = "bla";
    $b = "42";
    echo $a.$b
}
"""
ps=\
"""bla42"""

p=\
"""
{   
    $a = "bla";
    $b = "42";
    echo $a.$b
}
"""
ps=\
"""bla42"""

q=\
"""
{   
    $a = "bla";
    if True{
        echo "ummm";
    }
}
"""
qs=\
"""Error"""

r=\
"""
{   
    if (True){
        echo 1;
    }
    else {
    }
    IF (True){
    }
    ELSE {
    }
    If (True){
    }
    ELsE {
    }
    while (False){
    }
    WHILE (False){
    }
    wHilE (False){
    }
}
"""
rs=\
"""1"""

s=\
"""
{   
    if (True){
        echo 1;
    }
    else {
    }
    IF (True){
    }
    ELSE {
    }
    If (True){
    }
    ELsE {
    }
    while (False){
    }
    WHILE (False){
    }
    wHilE (False){
    }
}
"""
ss=\
"""1"""

t=\
"""
{   
    if (True){
        echo 1;
    }
    else {
    }
    else{
    }
}
"""
ts=\
"""Error"""


test = [a0,a,b,c,d,e,f,g,h,j,k,m,n,o,p,q,r,t]
sol = ["hello","hello!","hello2!","Error","hello","hello?","hello???","tudo certo","deu certo",\
    "certo2","certo3",ms,ns,os,ps,qs,rs,ts]

if (len(test) != len(sol)):
    raise Exception("len Sol != test")

init = 18
counter = init
while counter < (len(test) +init):
    print(counter)

    new_test = "new-test/teste{!s}.php".format(counter)
    with open(new_test, 'w') as file:
        file.write(test[counter - init])

    new_sol = "new-test/sol{!s}.txt".format(counter)
    with open(new_sol, 'w') as file:
        file.write(sol[counter - init])

    counter+=1


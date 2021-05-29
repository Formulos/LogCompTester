int main()
{
    int a;
    int b;
    a = 0;
    b = 1;
    while ((a < 99999) && (b ==1)){
        a = a +1;
        println(a);
        if (a == 5){
            b = 0;
        }
    }
    println(a);
}

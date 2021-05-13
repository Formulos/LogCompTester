{
    bool a;
    bool b;
    bool c;
    bool d;
    bool e;
    bool f;
    a = true;
    b = true;
    c = true;
    d = false;
    e = true;
    f = true;
    if (((a) || (b) || (c)) || ((d) && (e) && (f))){
        println(42);
    }
}

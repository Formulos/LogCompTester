int exibe(bool flag){
    if (flag){
        println(1);
    }else{
        println(0);
    }
}

/*OK: Parametro por variavel*/
int main(){
    bool f;
    f = true;
    exibe(f);
}

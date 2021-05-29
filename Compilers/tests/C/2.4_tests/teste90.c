int qualquer(){
    int x;
    x = 8;
    return x;
}

/*Erro: ja foi declarada funcao com este identificador*/
int qualquer(){
    int x;
    x = 10;
    return x;
}


int main(){
    int y;
    y = qualquer();
    println(y);
}

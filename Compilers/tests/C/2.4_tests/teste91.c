/*Erro: Declarar funcao dentro de funcao*/

int qualquer1(){
    int x;
    x = 10;
    
    int qualquer2(){
        int x;
        x = 8;
        
        return x;
    }
    
    return x;
}


int main(){
    int y;
    y = qualquer1();
    println(y);
}

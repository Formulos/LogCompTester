int serie(int x)
{
    if (x == 1) {
        return x;
    }else{
    	return x + serie(x-1);
    }
    
}

int main()
{
    int x;
    x = 5;
    println(serie(x));
    
}

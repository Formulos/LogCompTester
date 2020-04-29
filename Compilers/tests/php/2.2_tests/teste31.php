
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

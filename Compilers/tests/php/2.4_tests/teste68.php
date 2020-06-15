<?php
{
    function soma($x, $y) {
        function echoes($b) {
            echo $b;
            }
        $a = $x + $y;
        echoes($a);
        return $a;
        }
    $a = 3;
    echoes($a); /* ERROR: Soma nunca chamada = echoes não declarado */  
}
?>
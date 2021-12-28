<?php

$connect = pg_connect("host=localhost dbname=teste user=usario password=senha");
$lista = $_GET["lista"];
$query = "INSERT INTO infocc(name, quantity) VALUES ($name, $quantity);";
pg_query($connection, $query) or die("Error: ". pg_last_error(). "<br/>");

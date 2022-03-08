<?php
    header('Content-type: application/json');

    /* Require the Pinterest API class */
    require_once("Pinterest.class.php");

    // Create new instance of the Pinterest API
    $pinterest = new Pinterest("pinterest");
    $pinterest->itemsperpage = 50; // Default: 25

    // Check if a page has to be set
    if(isset($_GET['page'])){
        $pinterest->currentpage = (int) $_GET['page'];
    }

    // Check the action
    switch($_GET['action']){
         case "getboards":
             $resp = $pinterest->getBoards();
             break;
         case "getpinsfromboard":
             $resp = $pinterest->getPinsFromBoard($_GET["board"]);
             break;
         case "getpins":
         default:
             $resp = $pinterest->getPins();
             break;
     }

    // Return the data
    echo json_encode( $resp );
?>

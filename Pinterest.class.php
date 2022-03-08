<?php
/**
 * Pinterest API that collects the boards and/or pins from a user.
 *
 * This API has bene written because Pinterest doesn't have a public available API to get all the pins from a user.
 * The script uses two different API's. One for collecting the boards (pinterestapi.co.uk) and one for collection the pins from a board (Pinterest official).
 * To prevent a long waiting time caching has been applied.
 *
 * PHP version 5
 *
 * @author     Dirk Groenen <dirk@taketwo.nl>
 * @copyright  2014 - TakeTwo Merkidentiteit
 * @version    1.1.1
 */

class Pinterest {

    private $username;
    private $cacheprefix = "cache/pinterest_";
    public $itemsperpage = 50;
    public $currentpage = 1;
    
    /* 
     * Constructor that will set the username
     *
     * @param String $username
     */
    public function __construct($username)
    {
        $this->username = $username;
        
        // Check if the cache directory exists
        if(!file_exists(dirname(__FILE__) . "/cache")){
            mkdir(dirname(__FILE__) . "/cache", 0775);
        }
    }

    /* 
     * Get all the boards for the user
     *
     * @param boolean $intern
     * @return Array boards
     */
    public function getBoards($intern = false)
    {
        // Check for cache existence
        $cachedata = $this->getCache("boards_" . $this->username);
        if($cachedata == false)
        {
            // Create get request and put it in the cache
            $boards = $this->GET("http://pinterestapi.co.uk/" . $this->username . "/boards");


            // Get first pin from the board 
            foreach($boards->body as $board){
                $pinsdata = $this->getPinsFromBoard($board->href, true);

                // Get the image url and replace the board's src with the image from the pin
                $image = $pinsdata[0]->images->{'237x'}->url;
                $board->src = $image;
            }

            $this->putCache("boards_" . $this->username, json_encode($boards));
        }
        else
        {
            $boards = json_decode($cachedata);
        }
        
        return (!$intern) ? $this->buildResponse($boards->body) : $boards->body;
    }

    /*
     * Get pins from a single board
     *
     * @param string $board
     * @param boolean $intern
     * @return Json $pins
     */
    public function getPinsFromBoard($board, $intern = false)
    {
        // Check if the board is full url or just a single board name
        if(!preg_match("/\/(.*)\/(.*)\//", $board))
            $board = "/" . $this->username . "/" . $board . "/";

        // Check for cache existence
        $cachedata = $this->getCache($board);
        if($cachedata == false)
        {
            // Create get request and put it in the cache
            #$pins = $this->GET("https://api.pinterest.com/v3/pidgets/boards" . $board . "pins/");
            $pins = $this->GET("https://api.pinterest.com/v3/pidgets/boards/" . $this->username . "/" . $board . "/pins/");

            $this->putCache($board, json_encode($pins));
        }
        else
        {
            $pins = json_decode($cachedata);
        }
        
        // Check for failure
        if($pins->status == "failure"){
            throw new Exception("Board not found: " . $board);
        }
        
        return (!$intern) ? $this->buildResponse($pins->data->pins) : $pins->data->pins;
    }
    
    /*
     * Get all the user's pins (from all boards we can get)
     * Pins are sorted descending
     *
     * @return Json $pins
     */
    public function getPins()
    {
        // Init new array
        $pins = array();
    
        // Get all boards
        $boards = $this->getBoards(true);
        
        // Go through all boards
        foreach($boards as $board){
            // Request the pins from the board
            $pinsdata = $this->getPinsFromBoard($board->href, true);
            
            // Loop through all pins and put them in the pins array
            foreach($pinsdata as $pin){
                $pins[$pin->id] = $pin;
            }
        }
        
        // Sort the pins by key (desc)
        krsort($pins);
        
        //return $this->buildResponse($pins);
        return $this->buildResponse($pins);
    }
    
    /* 
     * Method to create a curl GET request
     *
     * @param string $url
     * @return JSON $response
     */
    private function GET($url)
    {
        // Get cURL resource
        $curl = curl_init();
        
        // Set some options - we are passing in a useragent too here
        curl_setopt_array($curl, array(
            CURLOPT_RETURNTRANSFER => 1,
            CURLOPT_URL => $url,
            CURLOPT_USERAGENT => 'TakeTwo API - Pinterest'
        ));
        
        // Send the request & save response to $resp
        $response = curl_exec($curl);
        
        // Close request to clear up some resources
        curl_close($curl);
        
        return json_decode($response);
    }
    
    /* 
     * Get the item from the cache if exists
     *
     * @param string $key
     * @return mixed $response
     */
    private function getCache($key)
    {
        $key = str_replace("/", "-", $key);
        $cache_file = dirname(__FILE__) . "/" . $this->cacheprefix . $key . ".cache";
        
        if (file_exists($cache_file) && (filemtime($cache_file) > (time() - 60 * 60 ))) 
        {
            // The cache is less than 60 minutes old so return the contents
            return file_get_contents($cache_file);
        } 
        else 
        {
            // The cache is older than 60 minutes to return FASLE
            return false;
        }
    }
    
    /* 
     * Put an item in the cache
     *
     * @param string $key
     * @return mixed $response
     * @return string $contents
     */
    private function putCache($key, $contents)
    {
        $key = str_replace("/", "-", $key);
        $cache_file =  dirname(__FILE__) . "/" . $this->cacheprefix . $key . ".cache";
    
        // Create a file and put the contents in it
        file_put_contents($cache_file, $contents, LOCK_EX);
        
        return $contents;
    }
    
    /* 
     * Build the response, wraps the data in some extra information like currentpage etc.
     *
     * @param Array $data
     * @return Array $response
     */
    private function buildResponse($data){

        $response = array(
            "total_items" => count($data),
            "items_per_page" => $this->itemsperpage,
            "total_pages" => ceil((count($data) / $this->itemsperpage)),
            "current_page" => $this->currentpage,
            "data" => array_slice($data, ($this->itemsperpage * ($this->currentpage = ($this->currentpage < 0) ? 0 : $this->currentpage - 1)), $this->itemsperpage)
        );
        
        return $response;
    }
    
};

?>
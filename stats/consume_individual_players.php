<?php
date_default_timezone_set('America/New_York');
/**
 * A simple example of how you could consume (ie: process) statuses collected by the ghetto-queue-collect.
 * 
 * This script in theory supports multi-processing assuming your filesystem supports flock() semantics. If you're not 
 * sure what that means, you probably don't need to worry about it :)
 * 
 * Caveat: I'm not sure if this works properly/at all on windows.
 * 
 * See: http://code.google.com/p/phirehose/wiki/Introduction
 */
class GhettoQueueConsumer1
{
  
  /**
   * Member attribs
   */
  protected $queueDir;
  protected $filePattern;
  protected $checkInterval;
  protected $usernameDB;
  protected $passwordDB;
  protected $database;
  protected $hostDB;
  protected $linkDB;
  
  /**
   * Construct the consumer and start processing
   */
  public function __construct($queueDir = '/tmp', $filePattern = 'phirehose-ghettoqueue*.queue', $checkInterval = 10)
  {
    $this->queueDir = $queueDir;
    $this->filePattern = $filePattern;
    $this->checkInterval = $checkInterval;
    
    // Sanity checks
    if (!is_dir($queueDir)) {
      throw new ErrorException('Invalid directory: ' . $queueDir);
    }
	
	$this->connectDB();
    
  }
  
  public function connectDB(){
	// open a conection to DB
	$this->usernameDB = '';
	$this->passwordDB = '';
	$this->hostDB = '';
	$this->database = '';
	$this->linkDB = mysql_connect($this->hostDB,$this->usernameDB,$this->passwordDB);
	mysql_select_db($this->database,$this->linkDB);	
  }
  
  /**
   * Method that actually starts the processing task (never returns).
   */
  public function process() {
    
    // Init some things
    $lastCheck = 0;
    
    // Loop infinitely
    while (TRUE) {
      
      // Get a list of queue files
      $queueFiles = glob($this->queueDir . '/' . $this->filePattern);
      $lastCheck = time();
      
      //$this->log('Found ' . count($queueFiles) . ' queue files to process...');
      
      // Iterate over each file (if any)
      foreach ($queueFiles as $queueFile) {
        $this->processQueueFile($queueFile);
      }
      
      // Wait until ready for next check
      //$this->log('Sleeping...');
      while (time() - $lastCheck < $this->checkInterval) {
        sleep(1);
      }
      
    } // Infinite loop
    
  } // End process()
  
  /**
   * Processes a queue file and does something with it (example only)
   * @param string $queueFile The queue file
   */
  protected function processQueueFile($queueFile) {
    //$this->log('Processing file: ' . $queueFile);
    
    // Open file
    $fp = fopen($queueFile, 'r');
    
    // Check if something has gone wrong, or perhaps the file is just locked by another process
    if (!is_resource($fp)) {
      //$this->log('WARN: Unable to open file or file already open: ' . $queueFile . ' - Skipping.');
      return FALSE;
    }
    
    // Lock file
    flock($fp, LOCK_EX);
    
    //get nascar id
    if( !$this->linkDB ):
		$this->log("Could not open DB connection.");
		do{
			$this->connectDB();
		}while( !$this->linkDB );
	endif;
    if($this->linkDB){
	    $group = mysql_query("select id from wp_bp_groups where name like 'nascar'",$this->linkDB);
	    $nascar_id = mysql_fetch_row($group);
	    $nascar_id = $nascar_id[0];
    }
    
    // Loop over each line (1 line per status)
    $statusCounter = 0;
    while ($rawStatus = fgets($fp, 8192)) {
    	$league = '';
      $statusCounter ++;
      
      /** **************** NOTE ********************
       * This is the part where you would normally do your processing. If you're extracting/trending information 
       * about the tweets it should happen here, where it doesn't matter so much if things are slow (you will
       * catch up on the next loop).
       */
      $data = json_decode($rawStatus, true);
      if (is_array($data) && isset($data['user']['screen_name'])) {
		// process tweet to DataBase
		if( !$this->linkDB ):
			$this->log("Could not open DB connection.");
			do{
				$this->connectDB();
			}while( !$this->linkDB );
		endif;
		if($this->linkDB):
			//first try to get from Tennis and Golf
			$results = mysql_query("select team_id, twitter_id, concat(firstname,' ',lastname) as name from wp_bp_individual_players where twitter = '".chop($data['user']['screen_name'])."';",$this->linkDB);
			if($results !== FALSE){
				$datas = mysql_fetch_row($results);
				//mysql_free_result($results);
				$league = $datas[0];
				$player = $datas[1];
				$bwn = $datas[2];
			}else{//if not in tennis of golf then look in nascar.
				$results = mysql_query("select twitter_id, concat(firstname,' ',lastname) as name from nascar_drivers where twitter = '".chop($data['user']['screen_name'])."';",$this->linkDB);
				if($results!==FALSE){
					$datas = mysql_fetch_row($results);
					//mysql_free_result($results);
					$league = $nascar_id;
					$player = $datas[0];
					$bwn = $datas[1];
				}else continue;
			}
			
			
			//get the team slug
			if( is_numeric($league) ){
				$result_ts = mysql_query("select if(c.parent_id > 0,concat((select p.slug from wp_bp_groups p where p.id = c.parent_id),'/',c.slug), c.slug) as groupslug, name from wp_bp_groups c where c.id = ".$league.";",$this->linkDB);
			
				$tas = mysql_fetch_row($result_ts);
				//mysql_free_result($result_ts);
				$team_slug = $tas[0];
				$team_name = $tas[1];
				$team_slug = "/groups/{$team_slug}";
				$action = "<strong>".addslashes($bwn)."</strong> posted an update in the team <a href='{$team_slug}''>{$team_name}</a>";

				if( is_numeric($league) && is_numeric($player) && strlen($action) > 0 ){
					$sql = "INSERT INTO wp_bp_twitter(user_id,component,type,action,content,primary_link,date_recorded,item_id,secondary_item_id,tweet_id,profile_picture,beat_writer) VALUES (1,'groups','twitter_update','".addslashes($action)."','".$data['user']['screen_name'].":".addslashes( urldecode($data['text']) )."','".$data['user']['screen_name']."','".date('Y-m-d H:i:s')."','$league','$player','".$data['id_str']."','".$data['user']['profile_image_url']."','false')";
					if($this->linkDB)$this->log($sql);
					else $this->log('Error: Could not connect to Database!');
					$this->log($sql);
					if(mysql_query($sql,$this->linkDB)){
						$this->log('Decoded tweet: ' . $data['user']['screen_name'] . ': ' . urldecode($data['text']) . ' -> League: ' . $league . ' | Player: ' . $player);
					}else{
						/*$f = fopen("/feeds/example/individual-players/errors.txt","w+");
						fwrite($f,'SQL => ' . $sql . "\n");
						fclose($f);*/
						$this->log('ERROR = ' . mysql_errno($this->linkDB) . ": " . mysql_error($this->linkDB). "\n");
					}
				}
			} // end is_numeric
		endif;
      }
      
    } // End while
    
    // Release lock and close
    flock($fp, LOCK_UN);
    fclose($fp);
    
    // All done with this file
    //$this->log('Successfully processed ' . $statusCounter . ' tweets from ' . $queueFile . ' - deleting.');
    if(file_exists($queueFile))
		unlink($queueFile);
  }
  
  /**
   * Basic log function.
   *
   * @see error_log()
   * @param string $messages
   */
  protected function log($message)
  {
    @error_log($message, 0);
  }
    
}

// Construct consumer and start processing
$gqc = new GhettoQueueConsumer1('/feeds/example/individual-players');
$gqc->process();
?>
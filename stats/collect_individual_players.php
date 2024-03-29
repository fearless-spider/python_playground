<?php
date_default_timezone_set('America/New_York');
require_once('/feeds/lib/Phirehose.php');
/**
 * Example of using Phirehose to collect tweets to a "ghetto queue" (ie: simple, filesystem based queue). 
 * This is not designed to be a production-ready/scalable collection system but is simple and does not rely on any
 * additional software or PHP modules. 
 * 
 * The idea with the ghetto queue is that a file is opened to collect tweets and rotate periodically to be processed by
 * a separate processing process. If you need "live" processing (ie: realtime auto-responses to tweets) you'd want to 
 * keep this low - ie: 5-10 seconds. If you're doing analytics, you should rotate less often (perhaps every hour or so).
 * 
 */
class GhettoQueueCollector extends Phirehose
{
  
  /**
   * Subclass specific constants
   */
  const QUEUE_FILE_PREFIX = 'phirehose-ghettoqueue';
  const QUEUE_FILE_ACTIVE = '.phirehose-ghettoqueue.current';
  
  /**
   * Member attributes specific to this subclass
   */
  protected $queueDir;
  protected $rotateInterval;
  protected $streamFile;
  protected $statusStream;
  protected $lastRotated;
  protected $usernameDB;
  protected $passwordDB;
  protected $database;
  protected $hostDB;
  protected $linkDB;
  
  /**
   * Overidden constructor to take class-specific parameters
   * 
   * @param string $username
   * @param string $password
   * @param string $queueDir
   * @param integer $rotateInterval
   */
  public function __construct($username, $password, $queueDir = '/tmp', $rotateInterval = 10)
  {
    
    // Sanity check
    if ($rotateInterval < 5) {
      throw new Exception('Rotate interval set too low - Must be >= 5 seconds');
    }
    
    // Set subclass parameters
    $this->queueDir = $queueDir;
    $this->rotateInterval = $rotateInterval;
	
	// open a conection to DB
	$this->usernameDB = '';
	$this->passwordDB = '';
	$this->hostDB = '';
	$this->database = '';
	$this->linkDB = mysql_connect($this->hostDB,$this->usernameDB,$this->passwordDB);
	mysql_select_db($this->database,$this->linkDB);
	
	
    
    // Call parent constructor
    return parent::__construct($username, $password, Phirehose::METHOD_FILTER);
  }
  
  public function connectDB($username,$password,$host){}
  
  /**
   * Enqueue each status
   *
   * @param string $status
   */
  public function enqueueStatus($status)
  {
    
    // Write the status to the stream (must be via getStream())
    fputs($this->getStream(), $status);

    /* Are we due for a file rotate? Note this won't be called if there are no statuses coming through - 
     * This is (probably) a good thing as it means the collector won't needlessly rotate empty files. That said, if
     * you have a very sparse/quiet stream that you need highly regular analytics on, this may not work for you. 
     */
    $now = time();
    if (($now - $this->lastRotated) > $this->rotateInterval) {
      // Mark last rotation time as now
      $this->lastRotated = $now;
      
      // Rotate it
      $this->rotateStreamFile();
    }
    
  }
  
  /**
   * Returns a stream resource for the current file being written/enqueued to
   * 
   * @return resource
   */
  private function getStream() 
  {
    // If we have a valid stream, return it
    if (is_resource($this->statusStream)) {
      return $this->statusStream;
    }
    
    // If it's not a valid resource, we need to create one
    if (!is_dir($this->queueDir) || !is_writable($this->queueDir)) {
      throw new Exception('Unable to write to queueDir: ' . $this->queueDir);
    }

    // Construct stream file name, log and open
    $this->streamFile = $this->queueDir . '/' . self::QUEUE_FILE_ACTIVE;
    $this->log('Opening new active status stream: ' . $this->streamFile);
    $this->statusStream = fopen($this->streamFile, 'a'); // Append if present (crash recovery)
    
    // Ok?
    if (!is_resource($this->statusStream)) {
      throw new Exception('Unable to open stream file for writing: ' . $this->streamFile);
    }
    
    // If we don't have a last rotated time, it's effectively now
    if ($this->lastRotated == NULL) {
      $this->lastRotated = time();
    }
    
    // Looking good, return the resource
    return $this->statusStream;
    
  }
  
  /**
   * Rotates the stream file if due
   */
  private function rotateStreamFile()
  {
    // Close the stream
    fclose($this->statusStream);
    
    // Create queue file with timestamp so they're both unique and naturally ordered
    $queueFile = $this->queueDir . '/' . self::QUEUE_FILE_PREFIX . '.' . date('Ymd-His') . '.queue';
    
    // Do the rotate
    rename($this->streamFile, $queueFile);
    
    // Did it work?
    if (!file_exists($queueFile)) {
      throw new Exception('Failed to rotate queue file to: ' . $queueFile);
    }
    
    // At this point, all looking good - the next call to getStream() will create a new active file
    $this->log('Successfully rotated active stream to queue file: ' . $queueFile);
  }
  
  /*
  ** select twitter id's from players
  */
  public function get_individual_twitter_id(){
	
	$data_ = array();
	if($this->linkDB):
		
		//Tennis and Golf
		$result_ = mysql_query("select twitter_id from wp_bp_individual_players where twitter_id is not null",$this->linkDB);
		while ($row = mysql_fetch_assoc($result_)) {
			$id = intval($row["twitter_id"]);
			if($id > 0){array_push($data_,$id);}
		}
		
		//Nascar
		$result_ = mysql_query("select twitter_id from nascar_drivers where twitter_id is not null and twitter_id != ''",$this->linkDB);
		while ($row = mysql_fetch_assoc($result_)) {
			$id = intval($row["twitter_id"]);
			if($id > 0){array_push($data_,$id);}
		}
	
		mysql_free_result($result_);
		mysql_close($this->linkDB);
		return $data_;
	endif;
	return FALSE;
  }

} // End of class

// Start streaming/collecting
$sc = new GhettoQueueCollector('', '', '/feeds/example/individual-players');
//$sc->setTrack(array('morning', 'goodnight', 'hello', 'the', 'and'));
$ids = $sc->get_individual_twitter_id();
if(is_array($ids)){
	$f = fopen("/feeds/example/individual-players/errors.txt","a");
	fwrite($f,"Twitters ready! \n");
	fwrite($f,implode(",",$ids)."\n");
	fclose($f);
	$sc->setFollow($ids);
	$sc->consume();	
}
?>
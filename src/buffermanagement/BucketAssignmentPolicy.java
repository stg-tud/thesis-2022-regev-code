package buffermanagement;

import core.DTNHost;
import core.Message;
import core.Settings;

public abstract class BucketAssignmentPolicy {
    int BucketCount;
    /**
     * Constructor
     */
    public BucketAssignmentPolicy(Settings s){
    }
/**
 * Assigns a destination Bucket to a message
 * @param m Message which should be assigned into a bucket
 * @param currentHost host, which receives or creates the message
 * @param receivedMessage indicator, whether host created or received the message
 * @return Index of the bucket, to which the message was assigned to
 */
    public abstract Integer assignBucket(Message m, DTNHost currentHost, Boolean receivedMessage);
/**
 * Returns the total amount of buckets the router has according to the current policy
 * @return total amount of buckets
 */
    public Integer getBucketCount(){
        return this.BucketCount;
    }

}

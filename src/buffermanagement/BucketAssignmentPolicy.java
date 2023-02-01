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

    public abstract Integer assignBucket(Message m, DTNHost currentHost);

    public Integer getBucketCount(){
        return this.BucketCount;
    }

}

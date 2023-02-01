package buffermanagement;

import core.Message;

public abstract class BucketAssignmentPolicy {
    
    /**
     * Constructor
     */
    public BucketAssignmentPolicy(){
    }

    public abstract int assignBucket(Message m);


}

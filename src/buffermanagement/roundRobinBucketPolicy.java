package buffermanagement;

import core.DTNHost;
import core.Message;
import core.Settings;

public class roundRobinBucketPolicy extends BucketAssignmentPolicy {
    int nextBucket = 0;
    public roundRobinBucketPolicy(Settings s) {
        super(s);
        this.BucketCount = 5;
    }

    @Override
    public Integer assignBucket(Message m, DTNHost currentHost, Boolean receivedMessage) {
        int retVal = this.nextBucket;
        this.nextBucket = (this.nextBucket + 1 ) % this.BucketCount;
        return retVal;
    }
    
}

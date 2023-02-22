package buffermanagement;

import core.DTNHost;
import core.Message;
import core.Settings;

public class destinationBasedBucketPolicy extends BucketAssignmentPolicy {

    public destinationBasedBucketPolicy(Settings s) {
        super(s);
        this.BucketCount = 2;
    }

    @Override
    public Integer assignBucket(Message m, DTNHost currentHost, Boolean receivedMessage) {
        if(currentHost.hasConnection(m.getTo())){
            return 0;
        }
        else{
            return 1;
        }
    }
    
}

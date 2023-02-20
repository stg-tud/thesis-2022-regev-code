package buffermanagement;

import core.DTNHost;
import core.Message;
import core.Settings;

public class senderBasedBucketAssignmentPolicy extends BucketAssignmentPolicy {

    public senderBasedBucketAssignmentPolicy(Settings s) {
        super(s);
        this.BucketCount = 3;
    }

    @Override
    public Integer assignBucket(Message m, DTNHost currentHost, Boolean receivedMessage) {
        if(m.getFrom().equals(currentHost)){
            return 0;
        }
        else if(m.getFrom().equals(m.getHops().get(0))){
            return 1;
        }
        else{
            return 2;
        }
    }
    
}

package buffermanagement;

import core.DTNHost;
import core.Message;
import core.Settings;

public class prioritizeLowTTLBucketPolicy extends BucketAssignmentPolicy{

    public prioritizeLowTTLBucketPolicy(Settings s) {
        super(s);
        this.BucketCount = 3;
    }

    @Override
    public Integer assignBucket(Message m, DTNHost currentHost, Boolean receivedMessage) {
        int messageTTL = m.getTtl();
        if(messageTTL < 150){
            return 0;
        }
        else if(messageTTL < 300){
            return 1;
        }
        else{
            return 2;
        }
    }
    
}

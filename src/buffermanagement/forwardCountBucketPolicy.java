package buffermanagement;

import core.DTNHost;
import core.Message;
import core.Settings;

public class forwardCountBucketPolicy extends BucketAssignmentPolicy {

    public forwardCountBucketPolicy(Settings s) {
        super(s);
        this.BucketCount = 4;
    }

    @Override
    public Integer assignBucket(Message m, DTNHost currentHost, Boolean receivedMessage) {
        if(m.getFrom().equals(currentHost)){
            return 0;
        }
        int forwardCount = m.getHopCount();
        if(forwardCount >= 9){
            return 0;
        }
        else if(forwardCount >= 6){
            return 1;
        }
        else if(forwardCount >= 3){
            return 2;
        }
        else{
            return 3;
        }
    }
    
}

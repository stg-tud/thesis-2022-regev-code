package buffermanagement;

import core.DTNHost;
import core.Message;
import core.Settings;

public class sourceSegregationBucketPolicy extends BucketAssignmentPolicy {

    public sourceSegregationBucketPolicy(Settings s){
        super(s);
        this.BucketCount = 1;
    }

    @Override
    public Integer assignBucket(Message m, DTNHost currentHost, Boolean receivedMessage) {
        if(m.getFrom().getAddress() % 2 == 0 || m.getFrom().equals(currentHost)){
            return 0;
        }
        else{
            return -1;
        }
    }
    
}

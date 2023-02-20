package buffermanagement;

import core.DTNHost;
import core.Message;
import core.Settings;

public class sizeBasedBucketsPolicy  extends BucketAssignmentPolicy{

    public sizeBasedBucketsPolicy(Settings s) {
        super(s);
        this.BucketCount = 4;
    }

    @Override
    public Integer assignBucket(Message m, DTNHost currentHost, Boolean receivedMessage) {
        int messageSize = m.getSize();
        if(messageSize < 500000){
            return 0;
        }
        else if(messageSize < 600000){
            return 1;
        }
        else if(messageSize < 750000){
            return 2;
        }
        else{
            return 3;
        }

    }
    
}

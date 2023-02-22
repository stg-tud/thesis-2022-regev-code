package buffermanagement;

import core.DTNHost;
import core.Message;
import core.Settings;
import java.util.concurrent.ThreadLocalRandom;

public class randomBucketPolicy extends BucketAssignmentPolicy {

    public randomBucketPolicy(Settings s) {
        super(s);
        this.BucketCount = 5;
    }

    @Override
    public Integer assignBucket(Message m, DTNHost currentHost, Boolean receivedMessage) {
        return ThreadLocalRandom.current().nextInt(0, this.BucketCount);
    }

    
}

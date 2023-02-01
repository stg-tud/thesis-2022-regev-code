package buffermanagement;
import core.DTNHost;
import core.Message;
import core.Settings;


public class DefaultBucketAssignmentPolicy extends BucketAssignmentPolicy{
    public DefaultBucketAssignmentPolicy(Settings s){
        super(s);
        this.BucketCount = 1;
    }
    @Override
    public Integer assignBucket(Message m, DTNHost currentHost) {
        return 0;
    }

    
}

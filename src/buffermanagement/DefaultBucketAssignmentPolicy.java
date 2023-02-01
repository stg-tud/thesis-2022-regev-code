package buffermanagement;
import core.Message;

public class DefaultBucketAssignmentPolicy extends BucketAssignmentPolicy{

    @Override
    public int assignBucket(Message m) {
        return 0;
    }
    
}

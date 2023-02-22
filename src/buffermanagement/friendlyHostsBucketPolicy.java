package buffermanagement;

import core.DTNHost;
import core.Message;
import core.Settings;

public class friendlyHostsBucketPolicy extends BucketAssignmentPolicy {

    public friendlyHostsBucketPolicy(Settings s) {
        super(s);
        this.BucketCount = 3;
    }

    @Override
    public Integer assignBucket(Message m, DTNHost currentHost, Boolean receivedMessage) {
        if(m.getFrom().equals(currentHost)){
            return 0;
        }
        else if(currentHost.getKnownHosts().contains(m.getFrom())){
            return 1;
        }
        else{
            return 2;
        }
    }
    
}

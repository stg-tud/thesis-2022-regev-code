package buffermanagement;

import core.Message;
import routing.MessageRouter;


public abstract class BucketPolicy {
    
    // determines bucket ID
    public abstract int determineBucketIDofMessage(MessageRouter router, Message incomingMessage);

    public abstract int determineBucketIDofMessageID(MessageRouter router, String messageID);

    public abstract int determineNextSendingBucket(MessageRouter router);

    public abstract int determineNumberofBuckets(MessageRouter router);
}

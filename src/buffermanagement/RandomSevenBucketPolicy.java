package buffermanagement;

import java.util.Random;

import core.Message;
import core.Settings;
import routing.MessageRouter;

public class RandomSevenBucketPolicy extends BucketPolicy {
    public RandomSevenBucketPolicy(Settings s) {
		super(s);
		// It doesn't need specific settings.
	}
    public int determineBucketIDofMessage(MessageRouter router, Message incomingMessage){
        if(incomingMessage == null){
            //System.out.println(incomingMessage);
            return 0;
        }
        /* 
        System.out.println("_______________");
        System.out.println(incomingMessage.getFrom().getAddress());
        System.out.println(incomingMessage.getFrom().getAddress() % 7);
        System.out.println("+++++++++++++++++");
        */
        return incomingMessage.getFrom().getAddress() % 7;


    }

    public int determineBucketIDofMessageID(MessageRouter router, String messageID){
        for(Message mtmp : router.getMessageCollection(-1)){
            if(mtmp.getId().equals(messageID)){
                return determineBucketIDofMessage(router, mtmp);
            }
        }
        return -1;
    }

    public int determineNextSendingBucket(MessageRouter router){
        Random rn = new Random();
        int i =rn.nextInt(6 - 0 + 1);
        return i;
    }

    public int determineNumberofBuckets(MessageRouter router){
        return 7;
    }
}

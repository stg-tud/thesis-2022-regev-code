package sendingpolicy;
import java.util.HashMap;
import java.util.List;

import core.Message;
import core.Settings;

/** Generic Class in order to implement the sorting mechanisms for the sending queues. Except MaxProp and Prophet Router */
public abstract class sendPolicy {
    public sendPolicy(Settings s){
    }

    public abstract HashMap<Integer, HashMap<String, Message>> sortQueueByPolicy(HashMap<Integer, HashMap<String, Message>> messages);
    
    public abstract List<Message>  sortMessageListByPolicy(List<Message> MessageBuffer);

    public abstract HashMap<String, Message>  sortBucketByPolicy(HashMap<String, Message> MessageBuffer);

    public abstract int compareMessagesByPolicy(Message m1, Message m2);
}


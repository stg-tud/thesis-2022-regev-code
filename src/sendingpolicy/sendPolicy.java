package sendingpolicy;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;

import core.Connection;
import core.Message;
import core.Settings;

/** Generic Class in order to implement the sorting mechanisms for the sending queues. Except MaxProp and Prophet Router */
public abstract class sendPolicy {
    public sendPolicy(Settings s){
    }
/**
 * receives a whole Buffer and sorts it according to the policy
 * @param messageBuffer message Buffer
 * @return sorted message Buffer
 */
    public abstract HashMap<Integer, HashMap<String, Message>> sortQueueByPolicy(HashMap<Integer, HashMap<String, Message>> messageBuffer);
/**
 * Receives List of Messages and sorts it according to the policy
 * @param messageList message List
 * @return sorted message List
 */  
    public abstract List<Message>  sortMessageListByPolicy(List<Message> messageList);
/**
 * Receives a single Bucket of the Buffer and sorts it according to the policy
 * @param MessageBucket Message Bucket
 * @return sorted Message Bucket
 */
    public abstract HashMap<String, Message>  sortBucketByPolicy(HashMap<String, Message> MessageBucket);
/**
 * Receives two messages and compares them. Returns int which indicates the order, according to the policy
 * @param m1 Message 1
 * @param m2 Message 2
 * @return Integer which indicates the order
 */
    public abstract int compareMessagesByPolicy(Message m1, Message m2);

/**
 * Receives a Hashset of connections and sorts them according to the policy
 * @param connections hashset of connections
 * @return sorted hashset of connections
 */
    public abstract HashSet<Connection> sortConnectionByPriority(HashSet<Connection> connections);
}


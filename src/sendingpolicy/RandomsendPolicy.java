package sendingpolicy;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.stream.Collectors;

import core.Connection;
import core.Message;
import core.Settings;
import core.SimClock;


public class RandomsendPolicy extends sendPolicy {

    public RandomsendPolicy(Settings s) {
        super(s);
    }

    @Override
    public LinkedHashMap<Integer, LinkedHashMap<String, Message>> sortQueueByPolicy(
        LinkedHashMap<Integer, LinkedHashMap<String, Message>> messages) {
                for(int i = 0; i < messages.size(); i++){
                    messages.put(i, sortBucketByPolicy(messages.get(i)));
                    
                }
                return messages;
    }

    public List<Message> sortMessageListByPolicy(List<Message> messageBuffer) {
        Map<Integer, List<Message>> bucketedMessages = new HashMap<>();
        for (Message m : messageBuffer) {
            Integer bucket = (Integer) m.getProperty("Bucket");
            if (bucket == null) {
                bucket = m.getFrom().getRouter().getCountBuckets();
            }
            bucketedMessages.computeIfAbsent(bucket, k -> new ArrayList<>()).add(m);
        }

        for (List<Message> messagesInBucket : bucketedMessages.values()) {
            Collections.shuffle(messagesInBucket, new Random(SimClock.getIntTime()));
        }

        List<Message> sortedMessages = new ArrayList<>();
        bucketedMessages.keySet().stream()
                .sorted()
                .forEach(bucket -> sortedMessages.addAll(bucketedMessages.get(bucket)));
    
        return sortedMessages;
    }
    

    @Override
    public LinkedHashMap<String, Message> sortBucketByPolicy(LinkedHashMap<String, Message> MessageBuffer) {
        LinkedHashMap<String, Message> ret = new LinkedHashMap<String, Message>();
        List<Message> msg = sortMessageListByPolicy(new ArrayList<Message>(MessageBuffer.values()));
        for(Message m : msg){
            ret.put(m.getId(), m);
        }
        return ret;
    }

    @Override
public int compareMessagesByPolicy(Message m1, Message m2) {
    Integer bucket1 = (Integer) m1.getProperty("Bucket");
    if (bucket1 == null) {
        bucket1 = m1.getFrom().getRouter().getCountBuckets();
    }

    Integer bucket2 = (Integer) m2.getProperty("Bucket");
    if (bucket2 == null) {
        bucket2 = m2.getFrom().getRouter().getCountBuckets();
    }

    if (!bucket1.equals(bucket2)) {
        return bucket1.compareTo(bucket2);
    }

    int hash_diff = m1.hashCode() - m2.hashCode();
    if (hash_diff == 0) {
        return 0;
    }
    return (hash_diff < 0 ? -1 : 1);
}


    @Override
    public LinkedHashSet<Connection> sortConnectionByPriority(LinkedHashSet<Connection> connections) {
        ArrayList<Connection> connectionList = (ArrayList<Connection>)connections.stream().collect(Collectors.toList());
        Collections.shuffle(connectionList, new Random(SimClock.getIntTime()));
        return new LinkedHashSet<Connection>(connectionList);
    }
    
}

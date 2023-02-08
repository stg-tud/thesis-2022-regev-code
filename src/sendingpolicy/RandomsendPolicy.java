package sendingpolicy;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
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
    public HashMap<Integer, HashMap<String, Message>> sortQueueByPolicy(
            HashMap<Integer, HashMap<String, Message>> messages) {
                for(int i = 0; i < messages.size(); i++){
                    messages.put(i, sortBucketByPolicy(messages.get(i)));
                    
                }
                return messages;
    }

    @Override
    public List<Message> sortMessageListByPolicy(List<Message> MessageBuffer) {
        Collections.shuffle(MessageBuffer, new Random(SimClock.getIntTime()));
        return MessageBuffer;
    }

    @Override
    public HashMap<String, Message> sortBucketByPolicy(HashMap<String, Message> MessageBuffer) {
        HashMap<String, Message> ret = new HashMap<String, Message>();
        List<Message> msg = sortMessageListByPolicy(new ArrayList<Message>(MessageBuffer.values()));
        for(Message m : msg){
            ret.put(m.getId(), m);
        }
        return ret;
    }

    @Override
    public int compareMessagesByPolicy(Message m1, Message m2) {
        int hash_diff = m1.hashCode() - m2.hashCode();
			if (hash_diff == 0) {
				return 0;
			}
			return (hash_diff < 0 ? -1 : 1);
    }

    @Override
    public HashSet<Connection> sortConnectionByPriority(HashSet<Connection> connections) {
        /*ArrayList<Connection> connectionList = (ArrayList<Connection>)connections.stream().collect(Collectors.toList());
        Collections.shuffle(connectionList, new Random(SimClock.getIntTime()));
        return new HashSet<Connection>(connectionList);
        */
        return connections;
    }
    
}

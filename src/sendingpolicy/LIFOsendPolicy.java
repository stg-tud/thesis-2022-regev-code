package sendingpolicy;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import util.Tuple;
import core.Connection;
import core.Message;
import core.Settings;
import core.SimError;

public class LIFOsendPolicy extends sendPolicy {

    public LIFOsendPolicy(Settings s) {
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

    @SuppressWarnings("unchecked")
    @Override
    public List<Message> sortMessageListByPolicy(List<Message> MessageBuffer) {
        Collections.sort(MessageBuffer,
					new Comparator() {
				/** Compares two tuples by their messages' receiving time */
				public int compare(Object o1, Object o2) {
					double diff;
					Message m1, m2;

					if (o1 instanceof Tuple) {
						m1 = ((Tuple<Message, Connection>)o1).getKey();
						m2 = ((Tuple<Message, Connection>)o2).getKey();
					}
					else if (o1 instanceof Message) {
						m1 = (Message)o1;
						m2 = (Message)o2;
					}
					else {
						throw new SimError("Invalid type of objects in " +
								"the list");
					}
                    Integer b1 = (Integer)m1.getProperty("Bucket");
                    Integer b2 = (Integer)m2.getProperty("Bucket");
                    if(b1 != null && b2 != null){
                        if(b1 < b2){
                            return -1;}
                        else if(b1 > b2){
                            return 1;}
                    }
					diff = m1.getReceiveTime() - m2.getReceiveTime();
					if (diff == 0) {
						return 0;
					}
					return (diff < 0 ? 1 : -1);
				}
			});
        return MessageBuffer;
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
        Integer b1 = (Integer)m1.getProperty("Bucket");
        Integer b2 = (Integer)m2.getProperty("Bucket");
            if(b1 != null && b2 != null){
                if(b1 < b2){
                    return -1;}
                else if(b1 > b2){
                    return 1;}
            }
        double diff = m1.getReceiveTime() - m2.getReceiveTime();
			if (diff == 0) {
				return 0;
			}
			return (diff < 0 ? 1 : -1);
    }

    @Override
    public LinkedHashSet<Connection> sortConnectionByPriority(LinkedHashSet<Connection> connections) {
        return connections;
    }
    
}

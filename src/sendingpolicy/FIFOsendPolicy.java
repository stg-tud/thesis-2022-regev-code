package sendingpolicy;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import util.Tuple;
import core.Connection;
import core.Message;
import core.Settings;
import core.SimError;

public class FIFOsendPolicy extends sendPolicy {

    public FIFOsendPolicy(Settings s) {
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

					diff = m1.getReceiveTime() - m2.getReceiveTime();
					if (diff == 0) {
						return 0;
					}
					return (diff < 0 ? -1 : 1);
				}
			});
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
        double diff = m1.getReceiveTime() - m2.getReceiveTime();
			if (diff == 0) {
				return 0;
			}
			return (diff < 0 ? -1 : 1);
    }
    
}

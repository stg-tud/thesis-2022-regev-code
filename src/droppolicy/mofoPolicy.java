package droppolicy;

import java.util.Collection;

import core.Message;
import core.Settings;
import routing.ActiveRouter;


public class mofoPolicy extends dropPolicy{
// MOFO => Drops the message with biggest forwardingcount
    public mofoPolicy(Settings s) {
        super(s);
    }

    @Override
    public Message determineNextMessageToRemove(ActiveRouter router, int bucket, boolean excludeMsgBeingSent) {
        Collection<Message> messages = router.getMessageCollection(bucket);
		Message biggestFWcount = null;
		for (Message m : messages) {

			if (excludeMsgBeingSent && router.isSending(m.getId())) {
				continue; // skip the message(s) that router is sending
			}

			if (biggestFWcount == null ) {
				biggestFWcount = m;
			}
			else if (biggestFWcount.getHopCount() < m.getHopCount()) {
				biggestFWcount = m;
			}
		}
        return biggestFWcount;
    }
    
}

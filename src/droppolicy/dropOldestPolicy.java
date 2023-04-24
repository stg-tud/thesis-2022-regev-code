package droppolicy;

import java.util.Collection;

import core.Message;
import core.Settings;
import routing.ActiveRouter;


public class dropOldestPolicy extends dropPolicy{
// Drop Oldest (DO) => Drops the message with the shortest TTL
    public dropOldestPolicy(Settings s) {
        super(s);
    }

    @Override
    public Message determineNextMessageToRemove(ActiveRouter router, int bucket, boolean excludeMsgBeingSent) {
        Collection<Message> messages = router.getMessageCollection(bucket);
		Message oldest = null;
		for (Message m : messages) {

			if (excludeMsgBeingSent && router.isSending(m.getId())) {
				continue; // skip the message(s) that router is sending
			}

			if (oldest == null ) {
				oldest = m;
			}
			else if (oldest.getTtl() > m.getTtl()) {
				oldest = m;
			}
		}
        return oldest;
    }
    
}

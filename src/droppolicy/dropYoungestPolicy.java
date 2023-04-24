package droppolicy;

import java.util.Collection;

import core.Message;
import core.Settings;
import routing.ActiveRouter;


public class dropYoungestPolicy extends dropPolicy{
// Drop Youngest (DY) => Drops the message with the longest TTL
    public dropYoungestPolicy(Settings s) {
        super(s);
    }

    @Override
    public Message determineNextMessageToRemove(ActiveRouter router, int bucket, boolean excludeMsgBeingSent) {
        Collection<Message> messages = router.getMessageCollection(bucket);
		Message youngest = null;
		for (Message m : messages) {

			if (excludeMsgBeingSent && router.isSending(m.getId())) {
				continue; // skip the message(s) that router is sending
			}

			if (youngest == null ) {
				youngest = m;
			}
			else if (youngest.getTtl() < m.getTtl()) {
				youngest = m;
			}
		}
        return youngest;
    }
    
}

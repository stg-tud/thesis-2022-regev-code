package droppolicy;

import java.util.Collection;

import core.Message;
import core.Settings;
import routing.ActiveRouter;


public class dropLargestPolicy extends dropPolicy{
// Drop Largest (DL) => Drops the largest message regarding size
    public dropLargestPolicy(Settings s) {
        super(s);
    }

    @Override
    public Message determineNextMessageToRemove(ActiveRouter router, int bucket, boolean excludeMsgBeingSent) {
        Collection<Message> messages = router.getMessageCollection(bucket);
		Message largest = null;
		for (Message m : messages) {

			if (excludeMsgBeingSent && router.isSending(m.getId())) {
				continue; // skip the message(s) that router is sending
			}

			if (largest == null ) {
				largest = m;
			}
			else if (largest.getSize() < m.getSize()) {
				largest = m;
			}
		}
        return largest;
    }
    
}

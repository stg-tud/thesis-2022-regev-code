package droppolicy;

import java.util.Collection;

import core.Message;
import core.Settings;
import routing.ActiveRouter;


public class dropLastPolicy extends dropPolicy{
// Drop Last (DL) => Drops the youngest message regarding receive time
    public dropLastPolicy(Settings s) {
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
			else if (youngest.getReceiveTime() < m.getReceiveTime()) {
				youngest = m;
			}
		}
        return youngest;
    }
    
}

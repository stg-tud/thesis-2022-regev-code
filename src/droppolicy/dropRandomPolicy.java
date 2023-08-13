package droppolicy;

import java.util.Collection;
import java.util.Random;
import core.Message;
import core.Settings;
import routing.ActiveRouter;


public class dropRandomPolicy extends dropPolicy{
// drop random => Drops the message randomly
    public dropRandomPolicy(Settings s) {
        super(s);
    }

    @Override
    public Message determineNextMessageToRemove(ActiveRouter router, int bucket, boolean excludeMsgBeingSent) {
        Collection<Message> messages = router.getMessageCollection(bucket);
        if(messages == null || messages.isEmpty()){
            return null;
        }
        else{
		return random(messages);
        }
    }
    public static <T> T random(Collection<T> coll) {
        int num = (int) (Math.random() * coll.size());
        for(T t: coll) if (--num < 0) return t;
        throw new AssertionError();
    }
}

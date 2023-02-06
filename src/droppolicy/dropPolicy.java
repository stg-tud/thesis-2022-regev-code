package droppolicy;

import core.Message;
import core.Settings;
import routing.ActiveRouter;

public abstract class dropPolicy {
    public dropPolicy(Settings s){}

    public abstract Message determineNextMessageToRemove(ActiveRouter router, int bucket, boolean excludeMsgBeingSent);
}

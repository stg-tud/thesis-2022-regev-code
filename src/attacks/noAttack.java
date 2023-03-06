package attacks;

import core.Connection;
import core.Message;
import core.Settings;

public class noAttack extends Attack{

    public noAttack(Settings s) {
        super(s);
        this.AttackType = -1;
    }

    @Override
    public Message attackOnMessage(Message m, Connection con) {
        return m;
    }

    @Override
    public Connection attackOnConnection(Message m, Connection con) {
        return con;
    }
    
}

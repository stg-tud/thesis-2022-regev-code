package attacks;

import core.Connection;
import core.Message;
import core.Settings;

public abstract class Attack {
    // 0=on Message , 1=in Connection
    int AttackType;
    public Attack(Settings s){
    }
    
    public abstract Message attackOnMessage(Message m, Connection con);

    public abstract Connection attackOnConnection(Message m, Connection con);

    public int getAttackType(){
        return this.AttackType;
    }
}

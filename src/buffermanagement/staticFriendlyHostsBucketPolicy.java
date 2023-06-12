package buffermanagement;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.Collection;
import java.util.Collections;
import java.util.HashMap;
import core.DTNHost;
import core.Message;
import core.Settings;




public class staticFriendlyHostsBucketPolicy extends BucketAssignmentPolicy {
    static HashMap<String,Integer> contact_policies;
    static int encounter_threshold = 999;
    public staticFriendlyHostsBucketPolicy(Settings s) throws IOException {
        super(s);
        this.BucketCount = 3;
        String contactPolicy = s.getSetting("contactPolicy");
        if(contact_policies == null){
            contact_policies = new HashMap<String, Integer>();
            try (BufferedReader br = new BufferedReader(new FileReader(contactPolicy))) {
                br.readLine();
                String line;
                while ((line = br.readLine()) != null) {
                    String[] vals = line.split(",");
                    contact_policies.put(vals[0], Integer.parseInt(vals[1]));
                }
                encounter_threshold = Collections.max(contact_policies.values()) / 2;
            } catch (Exception e) {
                e.printStackTrace();
            }
    
        }       
    }

    @Override
    public Integer assignBucket(Message m, DTNHost currentHost, Boolean receivedMessage) {
        int encounters = 0;
        if(contact_policies != null && contact_policies.containsKey(String.format("%s<->%s", m.getFrom(), currentHost.toString()))){
            encounters = contact_policies.get(String.format("%s<->%s", m.getFrom(), currentHost.toString()));
        }
        else if(contact_policies != null && contact_policies.containsKey(String.format("%s<->%s",currentHost.toString() ,m.getFrom()))){
            encounters = contact_policies.get(String.format("%s<->%s",currentHost.toString(), m.getFrom()));
        }
        if(m.getFrom().equals(currentHost)){
            return 0;
        }
        else if(encounters >= encounter_threshold){
            return 1;
        }
        else{
            return 2;
        }
    }
    
}

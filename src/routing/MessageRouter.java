/*
 * Copyright 2010 Aalto University, ComNet
 * Released under GPLv3. See LICENSE.txt for details.
 */
package routing;

import java.util.Collection;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Random;
import core.Application;
import core.Connection;
import core.DTNHost;
import core.Message;
import core.MessageListener;
import core.Settings;
import core.SettingsError;
import core.SimClock;
import core.SimError;
import routing.util.RoutingInfo;
import util.Tuple;
import buffermanagement.BucketPolicy;


/**
 * Superclass for message routers.
 */
public abstract class MessageRouter {
	/** Message buffer size -setting id ({@value}). Long value in bytes.*/
	public static final String B_SIZE_S = "bufferSize";
	/**
	 * Message TTL -setting id ({@value}). Value is in minutes and must be
	 * an integer.
	 */
	public static final String MSG_TTL_S = "msgTtl";
	/**
	 * Message/fragment sending queue type -setting id ({@value}).
	 * This setting affects the order the messages and fragments are sent if the
	 * routing protocol doesn't define any particular order (e.g, if more than
	 * one message can be sent directly to the final recipient).
	 * Valid values are<BR>
	 * <UL>
	 * <LI/> 1 : random (message order is randomized every time; default option)
	 * <LI/> 2 : FIFO (most recently received messages are sent last)
	 * </UL>
	 */
	public static final String SEND_QUEUE_MODE_S = "sendQueue";

		/**
	 * Bucket policy -setting id ({@value}). The class name used as the bucket
	 * policy implementation.
	 */
	public static final String BUCKET_POLICY_S = "bucketPolicy";

	int max_sending_id = 4;

	/** Setting value for random queue mode */
	public static final int Q_MODE_RANDOM = 1;
	/** Setting value for FIFO queue mode */
	public static final int Q_MODE_FIFO = 2;
	/** Setting value for LIFO queue mode */
	public static final int Q_MODE_LIFO = 3;
	/** Setting value for prioritized FIFO queue mode */
	public static final int Q_MODE_PFIFO = 4;

	/** Setting string for random queue mode */
	public static final String STR_Q_MODE_RANDOM = "RANDOM";
	/** Setting string for FIFO queue mode */
	public static final String STR_Q_MODE_FIFO = "FIFO";
	/** Setting string for LIFO queue mode */
	public static final String STR_Q_MODE_LIFO = "LIFO";
	/** Setting string for prioritized FIFO queue mode */
	public static final String STR_Q_MODE_PFIFO = "PFIFO";

	/* Return values when asking to start a transmission:
	 * RCV_OK (0) means that the host accepts the message and transfer started,
	 * values < 0 mean that the  receiving host will not accept this
	 * particular message (right now),
	 * values > 0 mean the host will not right now accept any message.
	 * Values in the range [-100, 100] are reserved for general return values
	 * (and specified here), values beyond that are free for use in
	 * implementation specific cases */
	/** Receive return value for OK */
	public static final int RCV_OK = 0;
	/** Receive return value for busy receiver */
	public static final int TRY_LATER_BUSY = 1;
	/** Receive return value for an old (already received) message */
	public static final int DENIED_OLD = -1;
	/** Receive return value for not enough space in the buffer for the msg */
	public static final int DENIED_NO_SPACE = -2;
	/** Receive return value for messages whose TTL has expired */
	public static final int DENIED_TTL = -3;
	/** Receive return value for a node low on some resource(s) */
	public static final int DENIED_LOW_RESOURCES = -4;
	/** Receive return value for a node low on some resource(s) */
	public static final int DENIED_POLICY = -5;
	/** Receive return value for unspecified reason */
	public static final int DENIED_UNSPECIFIED = -99;
	/** Maximum Ttl value */
	public static final int MAX_TTL_VALUE = 35791394;

	private List<MessageListener> mListeners;
	/** The messages being transferred with msgID_hostName keys */
	private HashMap<String, Message> incomingMessages;
	/** The messages this router is carrying */
	private HashMap<Integer, HashMap<String, Message>> messages = new HashMap<Integer, HashMap<String, Message>>();
	/** The messages this router has received as the final recipient */
	private HashMap<String, Message> deliveredMessages;
	/** The messages that Applications on this router have blacklisted */
	private HashMap<String, Object> blacklistedMessages;
	/** Host where this router belongs to */
	private DTNHost host;
	/** size of the buffer */
	private HashMap<Integer, Long> bufferSize = new HashMap<Integer, Long>();
	/** current occupancy of the buffer */
	private HashMap<Integer, Long> bufferOccupancy = new HashMap<Integer, Long>();
	/** TTL for all messages */
	protected int msgTtl;
	/** Queue mode for sending messages */
	private int sendQueueMode;
	/** The bucket policy used by the router. */
	private BucketPolicy bucketPolicy;

	/** applications attached to the host */
	private HashMap<String, Collection<Application>> applications = null;

	/**
	 * Constructor. Creates a new message router based on the settings in
	 * the given Settings object. Size of the message buffer is read from
	 * {@link #B_SIZE_S} setting. Default value is Integer.MAX_VALUE.
	 * @param s The settings object
	 */
	public MessageRouter(Settings s) {
		this.bufferSize.put(0, Long.valueOf(Integer.MAX_VALUE));// defaults to rather large buffer with default 1 shared buffer
		this.msgTtl = Message.INFINITE_TTL;
		this.applications = new HashMap<String, Collection<Application>>();

		if (s.contains(B_SIZE_S)) {
			this.bufferSize.put(0,s.getLong(B_SIZE_S));
		}
		// Create a bucket policy object if it is specified in the settings.
		if (s.contains(BUCKET_POLICY_S)) {
			String bucketPolicyClass = s.getSetting(BUCKET_POLICY_S);
			this.bucketPolicy = (BucketPolicy) s.createIntializedObject("buffermanagement." + bucketPolicyClass);
		}
		else {
			this.bucketPolicy = null;
		}
		if (s.contains(MSG_TTL_S)) {
			this.msgTtl = s.getInt(MSG_TTL_S);
			
			if (this.msgTtl > MAX_TTL_VALUE){
				throw new SettingsError("Invalid value for " + 
						s.getFullPropertyName(MSG_TTL_S) + 
								". Max value is limited to "+MAX_TTL_VALUE);
			}
		}
		if (s.contains(SEND_QUEUE_MODE_S)) {
			String mode = s.getSetting(SEND_QUEUE_MODE_S);
			if (mode.trim().toUpperCase().equals(STR_Q_MODE_FIFO)) {
				this.sendQueueMode = Q_MODE_FIFO;
			} else if (mode.trim().toUpperCase().equals(STR_Q_MODE_LIFO)) {
				this.sendQueueMode = Q_MODE_LIFO;
			} 	
			else if (mode.trim().toUpperCase().equals(STR_Q_MODE_RANDOM)){
				this.sendQueueMode = Q_MODE_RANDOM;
			} else if (mode.trim().toUpperCase().equals(STR_Q_MODE_PFIFO)){
				this.sendQueueMode = Q_MODE_PFIFO;
			}else {
				this.sendQueueMode = s.getInt(SEND_QUEUE_MODE_S);
				if (sendQueueMode < 1 || sendQueueMode > max_sending_id) {
					throw new SettingsError("Invalid value for " +
							s.getFullPropertyName(SEND_QUEUE_MODE_S));
				}
			}
		}
		else {
			sendQueueMode = Q_MODE_RANDOM;
		}
	}

	/**
	 * Initializes the router; i.e. sets the host this router is in and
	 * message listeners that need to be informed about message related
	 * events etc.
	 * @param host The host this router is in
	 * @param mListeners The message listeners
	 */
	public void init(DTNHost host, List<MessageListener> mListeners) {
		this.incomingMessages = new HashMap<String, Message>();
		this.deliveredMessages = new HashMap<String, Message>();
		this.blacklistedMessages = new HashMap<String, Object>();
		this.mListeners = mListeners;
		this.host = host;

		if (this.bucketPolicy == null){
			this.messages.put(0, new HashMap<String, Message>());
			this.bufferOccupancy.put(0,Long.valueOf(0));
		}
		else{
			for(int i = 0; i < this.bucketPolicy.determineNumberofBuckets(null); i++){
				this.messages.put(i, new HashMap<String, Message>());
				this.bufferOccupancy.put(i,Long.valueOf(0));
				this.bufferSize.put(i, Long.valueOf(Integer.MAX_VALUE));
			}
		}
	}

	/**
	 * Copy-constructor.
	 * @param r Router to copy the settings from.
	 */
	protected MessageRouter(MessageRouter r) {
		this.bufferSize = r.bufferSize;
		this.msgTtl = r.msgTtl;
		this.sendQueueMode = r.sendQueueMode;
		this.bucketPolicy = r.bucketPolicy;
		this.bufferOccupancy = r.bufferOccupancy;

		this.applications = new HashMap<String, Collection<Application>>();
		for (Collection<Application> apps : r.applications.values()) {
			for (Application app : apps) {
				addApplication(app.replicate());
			}
		}
	}

	/**
	 * Updates router.
	 * This method should be called (at least once) on every simulation
	 * interval to update the status of transfer(s).
	 */
	public void update(){
		for (Collection<Application> apps : this.applications.values()) {
			for (Application app : apps) {
				app.update(this.host);
			}
		}
	}

	/**
	 * Informs the router about change in connections state.
	 * @param con The connection that changed
	 */
	public abstract void changedConnection(Connection con);

	/**
	 * Returns a message by ID.
	 * @param id ID of the message
	 * @return The message
	 */
	protected Message getMessage(String messageId, int bucketID) {
		return this.messages.get(bucketID).get(messageId);
	}

	/**
	 * Checks if this router has a message with certain id buffered.
	 * @param id Identifier of the message
	 * @return True if the router has message with this id, false if not
	 */
	public boolean hasMessage(String messageID, int bucketID) {
		return this.messages.get(bucketID).containsKey(messageID);
	}

	/**
	 * Returns true if a full message with same ID as the given message has been
	 * received by this host as the <strong>final</strong> recipient
	 * (at least once).
	 * @param m message we're interested of
	 * @return true if a message with the same ID has been received by
	 * this host as the final recipient.
	 */
	protected boolean isDeliveredMessage(Message m) {
		return (this.deliveredMessages.containsKey(m.getId()));
	}

	/**
	 * Returns <code>true</code> if the message has been blacklisted. Messages
	 * get blacklisted when an application running on the node wants to drop it.
	 * This ensures the peer doesn't try to constantly send the same message to
	 * this node, just to get dropped by an application every time.
	 *
	 * @param id	id of the message
	 * @return <code>true</code> if blacklisted, <code>false</code> otherwise.
	 */
	protected boolean isBlacklistedMessage(String id) {
		return this.blacklistedMessages.containsKey(id);
	}

	/**
	 * Returns a reference to the messages of this router in collection.
	 * <b>Note:</b> If there's a chance that some message(s) from the collection
	 * could be deleted (or added) while iterating through the collection, a
	 * copy of the collection should be made to avoid concurrent modification
	 * exceptions.
	 * @return a reference to the messages of this router in collection
	 */
	public Collection<Message> getMessageCollection(int bucketID) {
		if (bucketID == -1){
			HashMap<String,Message> allMessages = new HashMap<String,Message>();
			for (int i = 0; i < this.messages.size() ; i++){
				allMessages.putAll(this.messages.get(i));
			}
			return allMessages.values();
		}		
		return this.messages.get(bucketID).values();
	}

	/**
	 * Returns the TOTAL (=sum of buckets) number of messages this router has
	 * @return How many messages this router has
	 */
	public int getNrofMessages() {
		int totalMessages = 0;
		for (int i = 0; i < this.messages.size(); i++){
			totalMessages += this.messages.get(i).size();;
		}
		return totalMessages;
	}

	/**
	 * Returns the size of the message buffer.
	 * @return The size or Integer.MAX_VALUE if the size isn't defined.
	 */
	//todo auch nach Bucket möglich machen
	public long getBufferSize(int bucketID) {
		if (bucketID == -1){
			long total = 0;
			for(int i = 0; i < this.bufferSize.size(); i++){
				total += this.bufferSize.get(i);
				return total;
			}
		}
		return this.bufferSize.get(bucketID);
	}

	/**
	 * Returns the amount of free space in the buffer. May return a negative
	 * value if there are more messages in the buffer than should fit there
	 * (because of creating new messages).
	 * @return The amount of free space (Integer.MAX_VALUE if the buffer
	 * size isn't defined)
	 */
	public long getFreeBufferSize(int bucketID) {
		if (bucketID == -1){
			long total = 0;
			long totalUsed = 0;
			for (int i = 0; i < this.bufferSize.size(); i++){
				total += this.bufferSize.get(i);
				totalUsed += this.bufferOccupancy.get(i);
				return total - totalUsed;
			}
		}
		if (this.getBufferSize(bucketID) == Integer.MAX_VALUE) {
			return Integer.MAX_VALUE;
		}

		return this.getBufferSize(bucketID) - this.bufferOccupancy.get(bucketID);
	}

	/**
	 * Returns the host this router is in
	 * @return The host object
	 */
	protected DTNHost getHost() {
		return this.host;
	}

	/**
	 * Start sending a message to another host.
	 * @param id Id of the message to send
	 * @param to The host to send the message to
	 */
	public void sendMessage(String id, DTNHost to, int bucketID) {
		Message m = getMessage(id, bucketID);
		Message m2;
		if (m == null) throw new SimError("no message for id " +
				id + " to send at " + this.host);

		m2 = m.replicate();	// send a replicate of the message
		to.receiveMessage(m2, this.host);
	}

	/**
	 * Requests for deliverable message from this router to be sent trough a
	 * connection.
	 * @param con The connection to send the messages trough
	 * @return True if this router started a transfer, false if not
	 */
	public boolean requestDeliverableMessages(Connection con) {
		return false; // default behavior is to not start -- subclasses override
	}

	/**
	 * Try to start receiving a message from another host.
	 * @param m Message to put in the receiving buffer
	 * @param from Who the message is from
	 * @return Value zero if the node accepted the message (RCV_OK), value less
	 * than zero if node rejected the message (e.g. DENIED_OLD), value bigger
	 * than zero if the other node should try later (e.g. TRY_LATER_BUSY).
	 */
	public int receiveMessage(Message m, DTNHost from) {
		Message newMessage = m.replicate();

		// TODO und wie gehts weiter vom IncomingBuffer? Dort die Logik einbauen
		this.putToIncomingBuffer(newMessage, from);
		newMessage.addNodeOnPath(this.host);

		for (MessageListener ml : this.mListeners) {
			ml.messageTransferStarted(newMessage, from, getHost());
		}

		return RCV_OK; // superclass always accepts messages
	}

	/**
	 * This method should be called (on the receiving host) after a message
	 * was successfully transferred. The transferred message is put to the
	 * message buffer unless this host is the final recipient of the message.
	 * @param id Id of the transferred message
	 * @param from Host the message was from (previous hop)
	 * @return The message that this host received
	 */
	public Message messageTransferred(String id, DTNHost from) {
		Message incoming = removeFromIncomingBuffer(id, from);
		boolean isFinalRecipient;
		boolean isFirstDelivery; // is this first delivered instance of the msg


		if (incoming == null) {
			throw new SimError("No message with ID " + id + " in the incoming "+
					"buffer of " + this.host);
		}

		incoming.setReceiveTime(SimClock.getTime());

		// Pass the message to the application (if any) and get outgoing message
		Message outgoing = incoming;
		for (Application app : getApplications(incoming.getAppID())) {
			// Note that the order of applications is significant
			// since the next one gets the output of the previous.
			outgoing = app.handle(outgoing, this.host);
			if (outgoing == null) break; // Some app wanted to drop the message
		}

		Message aMessage = (outgoing==null)?(incoming):(outgoing);
		// If the application re-targets the message (changes 'to')
		// then the message is not considered as 'delivered' to this host.
		isFinalRecipient = aMessage.getTo() == this.host;
		isFirstDelivery = isFinalRecipient &&
		!isDeliveredMessage(aMessage);

		if (!isFinalRecipient && outgoing!=null) {
			// not the final recipient and app doesn't want to drop the message
			// -> put to buffer
			addToMessages(aMessage, false);
		} else if (isFirstDelivery) {
			this.deliveredMessages.put(id, aMessage);
		} else if (outgoing == null) {
			// Blacklist messages that an app wants to drop.
			// Otherwise the peer will just try to send it back again.
			this.blacklistedMessages.put(id, null);
		}

		for (MessageListener ml : this.mListeners) {
			ml.messageTransferred(aMessage, from, this.host,
					isFirstDelivery);
		}

		return aMessage;
	}

	/**
	 * Puts a message to incoming messages buffer. Two messages with the
	 * same ID are distinguished by the from host.
	 * @param m The message to put
	 * @param from Who the message was from (previous hop).
	 */
	protected void putToIncomingBuffer(Message m, DTNHost from) {
		this.incomingMessages.put(m.getId() + "_" + from.toString(), m);
	}

	/**
	 * Removes and returns a message with a certain ID from the incoming
	 * messages buffer or null if such message wasn't found.
	 * @param id ID of the message
	 * @param from The host that sent this message (previous hop)
	 * @return The found message or null if such message wasn't found
	 */
	protected Message removeFromIncomingBuffer(String id, DTNHost from) {
		return this.incomingMessages.remove(id + "_" + from.toString());
	}

	/**
	 * Returns true if a message with the given ID is one of the
	 * currently incoming messages, false if not
	 * @param id ID of the message
	 * @return True if such message is incoming right now
	 */
	protected boolean isIncomingMessage(String id) {
		return this.incomingMessages.containsKey(id);
	}

	/**
	 * Returns true if router has currently any message in its incoming buffer,
	 * i.e., whether the router is currently receiving some message.
	 * @return true if incoming message buffer is not empty
	 */
	protected boolean hasIncomingMessage() {
		return !this.incomingMessages.isEmpty();
	}


	public int determineBucketIDofMessage(Message incomingMessage){
		if (this.bucketPolicy == null){
			return 0;
		}
		else{
			return this.bucketPolicy.determineBucketIDofMessage(this, incomingMessage);
		}
	}

	public int determineBucketIDofMessageID(String messageID){
		if (this.bucketPolicy == null){
			return 0;
		}
		else{
			return this.bucketPolicy.determineBucketIDofMessageID(this, messageID);
		}
	}

	public int determineNextSendingBucket(){
		if (this.bucketPolicy == null){
			return 0;
		}
		else{
			return this.bucketPolicy.determineNextSendingBucket(this);
		}
	}

	public int determineNumberofBuckets(){
		if (this.bucketPolicy == null){
			return 0;
		}
		else{
			return this.bucketPolicy.determineNumberofBuckets(this);
		}
	}

	/**
	 * Adds a message to the message buffer and informs message listeners
	 * about new message (if requested).
	 * @param m The message to add
	 * @param newMessage If true, message listeners are informed about a new
	 * message, if false, nothing is informed.
	 */
	protected void addToMessages(Message m, boolean newMessage) {
		int bucketID= determineBucketIDofMessage(m);
		this.messages.get(bucketID).put(m.getId(), m);
		this.bufferOccupancy.put(bucketID, this.bufferOccupancy.get(bucketID) + m.getSize());

		if (newMessage) {
			for (MessageListener ml : this.mListeners) {
				ml.newMessage(m);
			}
		}
	}

	/**
	 * Removes and returns a message from the message buffer.
	 * @param id Identifier of the message to remove
	 * @return The removed message or null if message for the ID wasn't found
	 */
	protected Message removeFromMessages(String id,int bucketID) {
		Message m = this.messages.get(bucketID).remove(id);
		this.bufferOccupancy.put(bucketID, this.bufferOccupancy.get(bucketID) - m.getSize());
		return m;
	}

	/**
	 * This method should be called (on the receiving host) when a message
	 * transfer was aborted.
	 * @param id Id of the message that was being transferred
	 * @param from Host the message was from (previous hop)
	 * @param bytesRemaining Nrof bytes that were left before the transfer
	 * would have been ready; or -1 if the number of bytes is not known
	 */
	public void messageAborted(String id, DTNHost from, int bytesRemaining) {
		Message incoming = removeFromIncomingBuffer(id, from);
		if (incoming == null) {
			throw new SimError("No incoming message for id " + id +
					" to abort in " + this.host);
		}

		for (MessageListener ml : this.mListeners) {
			ml.messageTransferAborted(incoming, from, this.host);
		}
	}

	/**
	 * Creates a new message to the router.
	 * @param m The message to create
	 * @return True if the creation succeeded, false if not (e.g.
	 * the message was too big for the buffer)
	 */
	public boolean createNewMessage(Message m) {
		m.setTtl(this.msgTtl);
		addToMessages(m, true);
		return true;
	}

	/**
	 * Deletes a message from the buffer and informs message listeners
	 * about the event
	 * @param id Identifier of the message to delete
	 * @param drop If the message is dropped (e.g. because of full buffer) this
	 * should be set to true. False value indicates e.g. remove of message
	 * because it was delivered to final destination.
	 */
	public void deleteMessage(String id,int bucketID ,boolean drop) {
		Message removed = removeFromMessages(id, bucketID);
		if (removed == null) throw new SimError("no message for id " +
				id + " to remove at " + this.host);

		for (MessageListener ml : this.mListeners) {
			ml.messageDeleted(removed, this.host, drop);
		}
	}

	/**
	 * Sorts/shuffles the given list according to the current sending queue
	 * mode. The list can contain either Message or Tuple<Message, Connection>
	 * objects. Other objects cause error.
	 * @param list The list to sort or shuffle
	 * @return The sorted/shuffled list
	 */
	@SuppressWarnings(value = "unchecked") /* ugly way to make this generic */
	protected List sortByQueueMode(List list) {
		switch (sendQueueMode) {
		case Q_MODE_RANDOM:
			Collections.shuffle(list, new Random(SimClock.getIntTime()));
			break;
		case Q_MODE_FIFO:
			Collections.sort(list,
					new Comparator() {
				/** Compares two tuples by their messages' receiving time */
				public int compare(Object o1, Object o2) {
					double diff;
					Message m1, m2;

					if (o1 instanceof Tuple) {
						m1 = ((Tuple<Message, Connection>)o1).getKey();
						m2 = ((Tuple<Message, Connection>)o2).getKey();
					}
					else if (o1 instanceof Message) {
						m1 = (Message)o1;
						m2 = (Message)o2;
					}
					else {
						throw new SimError("Invalid type of objects in " +
								"the list");
					}

					diff = m1.getReceiveTime() - m2.getReceiveTime();
					if (diff == 0) {
						return 0;
					}
					return (diff < 0 ? -1 : 1);
				}
			});
			break;
		/* add more queue modes here */
		case Q_MODE_LIFO:
			Collections.sort(list,
					new Comparator() {
				/** Compares two tuples by their messages' receiving time */
				public int compare(Object o1, Object o2) {
					double diff;
					Message m1, m2;

					if (o1 instanceof Tuple) {
						m1 = ((Tuple<Message, Connection>)o1).getKey();
						m2 = ((Tuple<Message, Connection>)o2).getKey();
					}
					else if (o1 instanceof Message) {
						m1 = (Message)o1;
						m2 = (Message)o2;
					}
					else {
						throw new SimError("Invalid type of objects in " +
								"the list");
					}

					diff = m1.getReceiveTime() - m2.getReceiveTime();
					if (diff == 0) {
						return 0;
					}
					return (diff > 0 ? -1 : 1);
				}
			});
			break;
		case Q_MODE_PFIFO: {
			Collections.sort(list,
					new Comparator() {
				/** Compares two tuples by their messages' receiving time */
				public int compare(Object o1, Object o2) {
					double diff;
					Message m1, m2;
					Object priority1, priority2;

					if (o1 instanceof Tuple) {
						m1 = ((Tuple<Message, Connection>)o1).getKey();
						m2 = ((Tuple<Message, Connection>)o2).getKey();
					}
					else if (o1 instanceof Message) {
						m1 = (Message)o1;
						m2 = (Message)o2;
					}
					else {
						throw new SimError("Invalid type of objects in " +
								"the list");
					}
					priority1 = m1.getProperty("PRIORITY");
					priority2 = m2.getProperty("PRIORITY");
					if(priority1 == null && priority2 == null){
						diff = m1.getReceiveTime() - m2.getReceiveTime();
						if (diff == 0) {
							return 0;
						}
						return (diff < 0 ? -1 : 1);
					}
					else if(priority1 == null && priority2 != null){
						return 1;
					}
					else if(priority1 != null && priority2 == null){
						return -1;
					}
					else {
						diff = m1.getReceiveTime() - m2.getReceiveTime();
						int pdiff = (int)priority1 - (int)priority2;
						if (pdiff == 0 && diff == 0){
							return 0;
						}
						else if(pdiff == 0){
							return (diff < 0 ? -1 : 1);
						}
						else {
							return (pdiff < 0 ? -1 : 1);
						}
					}
				}
			});
			break;



		}
		default:
			throw new SimError("Unknown queue mode " + sendQueueMode);
		}

		return list;
	}

	/**
	 * Gives the order of the two given messages as defined by the current
	 * queue mode
	 * @param m1 The first message
	 * @param m2 The second message
	 * @return -1 if the first message should come first, 1 if the second
	 *          message should come first, or 0 if the ordering isn't defined
	 */
	protected int compareByQueueMode(Message m1, Message m2) {
		switch (sendQueueMode) {
		case Q_MODE_RANDOM: {
			/* return randomly (enough) but consistently -1, 0 or 1 */
			int hash_diff = m1.hashCode() - m2.hashCode();
			if (hash_diff == 0) {
				return 0;
			}
			return (hash_diff < 0 ? -1 : 1);
		}
		case Q_MODE_FIFO: {
			double diff = m1.getReceiveTime() - m2.getReceiveTime();
			if (diff == 0) {
				return 0;
			}
			return (diff < 0 ? -1 : 1);
		}
		case Q_MODE_LIFO:{
			double diff = m1.getReceiveTime() - m2.getReceiveTime();
			if (diff == 0) {
				return 0;
			}
			return (diff > 0 ? -1 : 1);
		}
		case Q_MODE_PFIFO:{
			Object priority1 = m1.getProperty("PRIORITY");
			Object priority2 = m2.getProperty("PRIORITY");
			double diff = m1.getReceiveTime() - m2.getReceiveTime();
			if(priority1 == null && priority2 == null){
				if (diff == 0) {
					return 0;
				}
				return (diff < 0 ? -1 : 1);
			}
			else if(priority1 == null && priority2 != null){
				return 1;
			}
			else if(priority1 != null && priority2 == null){
				return -1;
			}
			else {
				int pdiff = (int)priority1 - (int)priority2;
				if (pdiff == 0 && diff == 0){
					return 0;
				}
				else if(pdiff == 0){
					return (diff < 0 ? -1 : 1);
				}
				else {
					return (pdiff < 0 ? -1 : 1);
				}
			}

		}
		/* add more queue modes here */
		default:
			throw new SimError("Unknown queue mode " + sendQueueMode);
		}
	}

	/**
	 * Returns routing information about this router.
	 * @return The routing information.
	 */
	public RoutingInfo getRoutingInfo() {
		RoutingInfo ri = new RoutingInfo(this);
		RoutingInfo incoming = new RoutingInfo(this.incomingMessages.size() +
				" incoming message(s)");
		RoutingInfo delivered = new RoutingInfo(this.deliveredMessages.size() +
				" delivered message(s)");

		RoutingInfo cons = new RoutingInfo(host.getConnections().size() +
			" connection(s)");

		ri.addMoreInfo(incoming);
		ri.addMoreInfo(delivered);
		ri.addMoreInfo(cons);

		for (Message m : this.incomingMessages.values()) {
			incoming.addMoreInfo(new RoutingInfo(m));
		}

		for (Message m : this.deliveredMessages.values()) {
			delivered.addMoreInfo(new RoutingInfo(m + " path:" + m.getHops()));
		}

		for (Connection c : host.getConnections()) {
			cons.addMoreInfo(new RoutingInfo(c));
		}

		return ri;
	}

	/**
	 * Adds an application to the attached applications list.
	 *
	 * @param app	The application to attach to this router.
	 */
	public void addApplication(Application app) {
		if (!this.applications.containsKey(app.getAppID())) {
			this.applications.put(app.getAppID(),
					new LinkedList<Application>());
		}
		this.applications.get(app.getAppID()).add(app);
	}

	/**
	 * Returns all the applications that want to receive messages for the given
	 * application ID.
	 *
	 * @param ID	The application ID or <code>null</code> for all apps.
	 * @return		A list of all applications that want to receive the message.
	 */
	public Collection<Application> getApplications(String ID) {
		LinkedList<Application>	apps = new LinkedList<Application>();
		// Applications that match
		Collection<Application> tmp = this.applications.get(ID);
		if (tmp != null) {
			apps.addAll(tmp);
		}
		// Applications that want to look at all messages
		if (ID != null) {
			tmp = this.applications.get(null);
			if (tmp != null) {
				apps.addAll(tmp);
			}
		}
		return apps;
	}

	/**
	 * Creates a replicate of this router. The replicate has the same
	 * settings as this router but empty buffers and routing tables.
	 * @return The replicate
	 */
	public abstract MessageRouter replicate();

	/**
	 * Returns a String presentation of this router
	 * @return A String presentation of this router
	 */
	public String toString() {

		return getClass().getSimpleName() + " of " +
			this.getHost().toString() + " with " + getNrofMessages()
			+ " messages";
	}
}

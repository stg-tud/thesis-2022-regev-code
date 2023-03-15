/*
 * Copyright 2010 Aalto University, ComNet
 * Released under GPLv3. See LICENSE.txt for details.
 */
package report;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Set;

import core.Settings;
import core.SimClock;
import core.SimError;
import core.SimScenario;

/**
 * Abstract superclass for all reports. All settings defined in this class
 * can be used for all Report classes. Some reports don't implement intervalled
 * reports ({@link #INTERVAL_SETTING}) and will ignore that setting. Most of
 * the reports implement warm up feature ({@link #WARMUP_S}) but the
 * implementations are always report specific.
 */
public abstract class Report {
	/** Name space of the settings that are common to all reports ({@value}). */
	public static final String REPORT_NS = "Report";
	/** The interval (simulated seconds) of creating new settings files
	 * -setting id ({@value}) */
	public static final String INTERVAL_SETTING = "interval";
	/** The output file path of the report -setting id ({@value})*/
	public static final String OUTPUT_SETTING = "output";
	/** Precision of formatted double values - setting id ({@value}).
	 * Defines the amount of decimals shown in formatted double values.
	 * Default value is {@value #DEF_PRECISION}. */
	public static final String PRECISION_SETTING = "precision";
	/** Default precision of formatted double values */
	public static final int DEF_PRECISION = 4;
	/** The default output directory of reports (can be overridden per report
	 * with {@link Report#OUTPUT_SETTING}) -setting id ({@value})*/
	public static final String REPORTDIR_SETTING = "Report.reportDir";
	/** Warm up period -setting id ({@value}). Defines how many seconds from
	 *  the beginning of the simulation should not be included in the reports.
	 *  Implementation of the feature is report specific, so check out the
	 *  respective report classes for details. Default is 0. Must be a positive
	 *  integer or 0. */
	public static final String WARMUP_S = "warmup";
	/** Suffix of report files without explicit output */
	public static final String OUT_SUFFIX = ".txt";
	/** Suffix for reports that are created on n second intervals */
	public static final String INTERVALLED_FORMAT ="%04d" + OUT_SUFFIX;
	/** The print writer used to write output. See {@link #write(String)} */
	protected PrintWriter out;
	/** String value for values that could not be calculated */
	public static final String NAN = "NaN";
	private String prefix = "";
	private int precision;
	protected int warmupTime;
	protected Set<String> warmupIDs;


	private int lastOutputSuffix;
	private double outputInterval;
	private double lastReportTime;
	private String outFileName;
	private String scenarioName;

	public static final String GROUP_NS = "Group";
	public int MAX_GROUPIDs;
	public static final String NR_GROUPS_S = "Scenario.nrofHostGroups";
	public static final String defaultPolicy = "Default";
	public LinkedHashMap<String,String> groupInfos;
	/**
	 * Settings Identifier for Bucket Policy
	 */
	public static final String BUCKET_POLICY_S = "BucketPolicy";
	private LinkedHashMap<String,String> bucketPolicy;
	private static final String defaultBucketPolicy = "DefaultBucketAssignmentPolicy";

	/**
	 * Settings Identifier for Sending Policy
	 */
	public static final String SENDING_POLICY_S = "SendingPolicy";
	private LinkedHashMap<String,String> sendingPolicy;
	private static final String defaultSendingPolicy = "DefaultsendPolicy";

	/**
	 * Settings Identifier for Drop Policy
	 */
	public static final String DROP_POLICY_S = "DropPolicy";
	private LinkedHashMap<String,String> dropPolicy;
	private static final String defaultDropPolicy = "defaultDropPolicy";

	public static final String ROUTER_S = "router";
	private LinkedHashMap<String,String> routerList;


	public static final String EVENT_NS = "Events";
	private LinkedHashMap<String,String> eventInfos;
	/**
	 * Constructor.
	 * Looks for a className.output setting in the Settings and
	 * if such is found, uses that as the output file name. Otherwise
	 * scenarioname_classname.txt is used as the file name.
	 */
	public Report(){
		this.lastOutputSuffix = 0;
		this.outputInterval = -1;
		this.warmupIDs = null;

		Settings settings = new Settings();
		scenarioName = settings.valueFillString(settings.getSetting(
				SimScenario.SCENARIO_NS + "." +	SimScenario.NAME_S));
		settings = getSettings();

		if(settings.containsNoNamespace(NR_GROUPS_S)){
			this.MAX_GROUPIDs = Integer.parseInt(settings.getSettingNoNamespace(NR_GROUPS_S));
		}
		else{
			this.MAX_GROUPIDs = 9;
		}
		this.groupInfos = new LinkedHashMap<String,String>();
		this.bucketPolicy = new LinkedHashMap<String,String>();
		this.sendingPolicy = new LinkedHashMap<String,String>();
		this.dropPolicy = new LinkedHashMap<String,String>();
		this.routerList = new LinkedHashMap<String,String>();

		// Reading out of Group Router and Infos + drop, sending and bucket policies
		for(int i=0; i <= MAX_GROUPIDs; i++){
			String ix = Integer.toString(i);
			if(i == 0){
				ix = "";
			}
			if(settings.containsNoNamespace(GROUP_NS + ix + "." + ROUTER_S)){
				this.routerList.put(GROUP_NS + ix, settings.getSettingNoNamespace(GROUP_NS + ix + "." + ROUTER_S));
				readPolicies(ix,settings);
				if(settings.containsNoNamespace(GROUP_NS + ix + "." + "bufferSize")){
					this.groupInfos.put(GROUP_NS + ix + "." + "bufferSize",settings.getSettingNoNamespace(GROUP_NS + ix + "." + "bufferSize"));
				}
				if(settings.containsNoNamespace(GROUP_NS + ix + "." + "waitTime")){
					this.groupInfos.put(GROUP_NS + ix + "." + "waitTime",settings.getSettingNoNamespace(GROUP_NS + ix + "." + "waitTime"));
				}
				if(settings.containsNoNamespace(GROUP_NS + ix + "." + "nrofInterfaces")){
					this.groupInfos.put(GROUP_NS + ix + "." + "nrofInterfaces",settings.getSettingNoNamespace(GROUP_NS + ix + "." + "nrofInterfaces"));
				}
				if(settings.containsNoNamespace(GROUP_NS + ix + "." + "speed")){
					this.groupInfos.put(GROUP_NS + ix + "." + "speed",settings.getSettingNoNamespace(GROUP_NS + ix + "." + "speed"));
				}
				if(settings.containsNoNamespace(GROUP_NS + ix + "." + "msgTtl")){
					this.groupInfos.put(GROUP_NS + ix + "." + "msgTtl",settings.getSettingNoNamespace(GROUP_NS + ix + "." + "msgTtl"));
				}
				if(settings.containsNoNamespace(GROUP_NS + ix + "." + "nrofHosts")){
					this.groupInfos.put(GROUP_NS + ix + "." + "nrofHosts",settings.getSettingNoNamespace(GROUP_NS + ix + "." + "nrofHosts"));
				}
			}
			else{
				break;
			}
		}
		this.eventInfos = new LinkedHashMap<String,String>();
		if(settings.containsNoNamespace(EVENT_NS + "." + "nrof")){
			for(int ix=1; ix <= Integer.parseInt(settings.getSettingNoNamespace(EVENT_NS + "." + "nrof")); ix++){
				if(settings.containsNoNamespace(EVENT_NS + ix + "." + "class")){
					this.eventInfos.put(EVENT_NS + ix + "." + "class",settings.getSettingNoNamespace(EVENT_NS + ix + "." + "class"));
				}
				if(settings.containsNoNamespace(EVENT_NS + ix + "." + "interval")){
					this.eventInfos.put(EVENT_NS + ix + "." + "interval",settings.getSettingNoNamespace(EVENT_NS + ix + "." + "interval"));
				}
				if(settings.containsNoNamespace(EVENT_NS + ix + "." + "size")){
					this.eventInfos.put(EVENT_NS + ix + "." + "size",settings.getSettingNoNamespace(EVENT_NS + ix + "." + "size"));
				}
				if(settings.containsNoNamespace(EVENT_NS + ix + "." + "hosts")){
					this.eventInfos.put(EVENT_NS + ix + "." + "hosts",settings.getSettingNoNamespace(EVENT_NS + ix + "." + "hosts"));
				}
			}

		}
		if (settings.contains(INTERVAL_SETTING)) {
			outputInterval = settings.getDouble(INTERVAL_SETTING);
		}

		if (settings.contains(WARMUP_S)) {
			this.warmupTime = settings.getInt(WARMUP_S);
		}
		else {
			this.warmupTime = 0;
		}


		if (settings.contains(PRECISION_SETTING)) {
			precision = settings.getInt(PRECISION_SETTING);
			if (precision < 0) {
				precision = 0;
			}
		}
		else {
			precision = DEF_PRECISION;
		}

		if (settings.contains(OUTPUT_SETTING)) {
			outFileName = settings.getSetting(OUTPUT_SETTING);
			// fill value place holders in the name
			outFileName = settings.valueFillString(outFileName);
		}
		else {
			// no output name define -> construct one from report class' name
			settings.setNameSpace(null);
			String outDir = settings.getSetting(REPORTDIR_SETTING);
			if (!outDir.endsWith("/")) {
				outDir += "/";	// make sure dir ends with directory delimiter
			}
			outFileName = outDir + scenarioName +
				"_" + this.getClass().getSimpleName();
			if (outputInterval == -1) {
				outFileName += OUT_SUFFIX; // no intervalled reports
			}

		}

		checkDirExistence(outFileName);
	}

	/**
	 * Checks that a directory for a file exists or creates the directory
	 * if it didn't exist.
	 * @param outFileName Name of the file
	 */
	private void checkDirExistence(String outFileName) {
		File outFile = new File(outFileName);
		File outDir = outFile.getParentFile();

		if (outDir != null && !outDir.exists()) {
			if (!createDirs(outDir)) {
				throw new SimError("Couldn't create report directory '" +
						outDir.getAbsolutePath()+"'");
			}
		}
	}

	/**
	 * Recursively creates a directory structure
	 * @param directory The directory to create
	 * @return True if the creation succeeded, false if not
	 */
	private boolean createDirs(File directory) {
		if (directory==null) {
			return true;
		}
		if (directory.exists()) {
			return true;
		} else {
			if (!createDirs(directory.getParentFile())) {
				return false;
			}
			if (!directory.mkdir()) {
				return false;
			} else {
				return true;
			}
		}
	}

	/**
	 * Initializes the report output. Method is called in the beginning of
	 * every new report file. Subclasses must call this method first in their
	 * own implementations of init().
	 */
	protected void init() {
		this.lastReportTime = getSimTime();

		if (outputInterval > 0) {
			createSuffixedOutput(outFileName);
		}
		else {
			createOutput(outFileName);
		}
	}

	/**
	 * Creates a new output file
	 * @param outFileName Name (&path) of the file to create
	 */
	private void createOutput(String outFileName) {
		try {
			this.out = new PrintWriter(new FileWriter(outFileName));
		} catch (IOException e) {
			throw new SimError("Couldn't open file '" + outFileName +
					"' for report output\n" + e.getMessage(), e);
		}
	}

	/**
	 * Creates a number-suffixed output file with increasing number suffix
	 * @param outFileName Prefix of the output file's name
	 */
	private void createSuffixedOutput(String outFileName) {
		String suffix = String.format(INTERVALLED_FORMAT,
				this.lastOutputSuffix);
		createOutput(outFileName+suffix);
		this.lastOutputSuffix++;
	}

	/**
	 * This method should be called before every new (complete) event the
	 * report logs. If the report has no meaningful use for multiple reports,
	 * the call can be omitted (then only single output file will be generated)
	 */
	protected void newEvent() {
		if (this.outputInterval <= 0) {
			return;
		}

		if (getSimTime() > this.lastReportTime + this.outputInterval) {
			done(); // finalize the old file
			init(); // init the new file
		}
	}

	/**
	 * Writes a line to report using defined prefix and {@link #out} writer.
	 * @param txt Line to write
	 * @see #setPrefix(String)
	 */
	protected void write(String txt) {
		if (out == null) {
			init();
		}
		out.println(prefix + txt);
	}

	/**
	 * Formats a double value according to current precision setting (see
	 * {@link #PRECISION_SETTING}) and returns it in a string.
	 * @param value The value to format
	 * @return Formatted value in a string
	 */
	protected String format(double value) {
		return String.format("%." + precision + "f", value);
	}

	/**
	 * Sets a prefix that will be inserted before every line in the report
	 * @param txt Text to use as the prefix
	 */
	protected void setPrefix(String txt) {
		this.prefix = txt;
	}

	/**
	 * Returns the name of the scenario as read from the settings
	 * @return the name of the scenario as read from the settings
	 */
	protected String getScenarioName() {
		return this.scenarioName;
	}

	protected void readPolicies(String ix, Settings settings){
		String bucketID = GROUP_NS + ix + "." + BUCKET_POLICY_S;
		String dropID = GROUP_NS + ix + "." + DROP_POLICY_S;
		String sendingID = GROUP_NS + ix + "." + SENDING_POLICY_S;


		if (settings.containsNoNamespace(bucketID) && !settings.getSettingNoNamespace(bucketID).equals(defaultBucketPolicy)) {
			this.bucketPolicy.put(GROUP_NS + ix,settings.getSettingNoNamespace(bucketID));
		}
		else {
			this.bucketPolicy.put(GROUP_NS + ix, defaultPolicy);
		}
		if (settings.containsNoNamespace(dropID) && !settings.getSettingNoNamespace(dropID).equals(defaultDropPolicy)) {
			this.dropPolicy.put(GROUP_NS + ix, settings.getSettingNoNamespace(dropID));
		}
		else {
			this.dropPolicy.put(GROUP_NS + ix, defaultPolicy);
		}
		if (settings.containsNoNamespace(sendingID) && !settings.getSettingNoNamespace(sendingID).equals(defaultSendingPolicy)) {
			this.sendingPolicy.put(GROUP_NS + ix, settings.getSettingNoNamespace(sendingID));
		}
		else {
			this.sendingPolicy.put(GROUP_NS + ix, defaultPolicy);
		}
	}
	/**
	 * Returns the list of the names of the bucketPolicies
	 * @return bucketPolicy List
	 */
	protected LinkedHashMap<String,String> getBucketPolicy(){
		return this.bucketPolicy;
	}

	/**
	 * Returns the list of the names of the getSendingPolicies
	 * @return getSendingPolicy List
	 */
	protected LinkedHashMap<String,String> getSendingPolicy(){
		return this.sendingPolicy;
	}
	/**
	 * Returns the list of the names of the dropPolicies
	 * @return dropPolicy List
	 */
	protected LinkedHashMap<String,String> getDropPolicy(){
		return this.dropPolicy;
	}

	/**
	 * Returns a list of the present router groups
	 * @return list of router groups
	 */
	protected LinkedHashMap<String,String> getRouterList(){
		return this.routerList;
	}

	/**
	 * Returns a list of relevant Events Infos
	 * @return relevant Events Infos
	 */
	protected LinkedHashMap<String,String> getEventsInfo(){
		return this.eventInfos;
	}

	/**
	 * Returns a list of relevant Group Infos
	 * @return relevant Group Infos
	 */
	protected LinkedHashMap<String,String> getGroupInfo(){
		return this.groupInfos;
	}
	/**
	 * Returns the current simulation time from the SimClock
	 * @return the current simulation time from the SimClock
	 */
	protected double getSimTime() {
		return SimClock.getTime();
	}

	/**
	 * Returns true if the warm up period is still ongoing (simTime < warmup)
	 * @return true if the warm up period is still ongoing, false if not
	 */
	protected boolean isWarmup() {
		return this.warmupTime > SimClock.getTime();
	}

	/**
	 * Adds a new ID to the warm up ID set
	 * @param id The ID
	 */
	protected void addWarmupID(String id) {
		if (this.warmupIDs == null) { // lazy creation of the Set
			this.warmupIDs = new HashSet<String>();
		}

		this.warmupIDs.add(id);
	}

	/**
	 * Removes a warm up ID from the warm up ID set
	 * @param id The ID to remove
	 */
	protected void removeWarmupID(String id) {
		this.warmupIDs.remove(id);
	}

	/**
	 * Returns true if the given ID is in the warm up ID set
	 * @param id The ID
	 * @return true if the given ID is in the warm up ID set
	 */
	protected boolean isWarmupID(String id) {
		if (this.warmupIDs == null || this.warmupIDs.size() == 0) {
			return false;
		}

		return this.warmupIDs.contains(id);
	}

	/**
	 * Returns a Settings object initialized for the report class' name space
	 * that uses {@value REPORT_NS} as the secondary name space.
	 * @return a Settings object initialized for the report class' name space
	 */
	protected Settings getSettings() {
		Settings s = new Settings(this.getClass().getSimpleName());
		s.setSecondaryNamespace(REPORT_NS);
		return s;
	}

	/**
	 * Called when the simulation is done, user requested
	 * premature termination or intervalled report generating decided
	 * that it's time for the next report.
	 */
	public void done() {
		if (out != null) {
			out.close();
		}
	}

	/**
	 * Returns the average of double values stored in a List or "NaN" for
	 * empty lists.
	 * @param values The list of double values
	 * @return average of double values stored in the List in a formatted String
	 */
	public String getAverage(List<Double> values) {
		double sum = 0;
		if (values.size() == 0) {
			return NAN;
		}

		for (double dValue : values) {
			sum += dValue;
		}

		return format(sum / values.size());
	}

	/**
	 * Returns the average of integer values stored in a List
	 * @param values The list of values
	 * @return average of integer values stored in the List or "NaN" for
	 * empty lists.
	 */
	public String getIntAverage(List<Integer> values) {
		List<Double> dValues = new ArrayList<Double>(values.size());
		for (int i : values) {
			dValues.add((double)i);
		}
		return getAverage(dValues);
	}

	/**
	 * Returns the median of double values stored in a List
	 * @param values The list of double values
	 * @return median of double values stored in the List or "NaN" for
	 * empty lists.
	 */
	public String getMedian(List<Double> values) {
		if (values.size() == 0) {
			return NAN;
		}

		Collections.sort(values);
		return format(values.get(values.size()/2));
	}

	/**
	 * Returns the median of integer values stored in a List
	 * @param values The list of values
	 * @return median of integer values stored in the List or 0 for
	 * empty lists.
	 */
	public int getIntMedian(List<Integer> values) {
		if (values.size() == 0) {
			return 0;
		}

		Collections.sort(values);
		return values.get(values.size()/2);
	}

	/**
	 * Returns the variance of the values in the List.
	 *
	 * @param values	The list of values
	 * @return The variance of the values in the list or "NaN" if the list is
	 * empty.
	 */
	public String getVariance(List<Double> values) {
		if (values.size()==0) return "NaN";
		double E_X;
		double sum=0, sum2=0;
		for (double dValue : values) {
			sum += dValue;
			sum2 += dValue*dValue;
		}
		E_X = sum / values.size();
		return format(sum2/values.size() - (E_X*E_X));
	}

}

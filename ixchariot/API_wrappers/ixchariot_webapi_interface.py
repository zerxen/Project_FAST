# -*- coding: utf-8 -*-
from vspk import v4_0 as vsdk
from pprint import pprint
from .ixchariot_access_configuration import ixchariot_configuration
from ixchariot.webapi.ixia.webapi import *
import ixchariot.webapi.ixchariotApi as ixchariotApi
from nuage.API_wrappers.nuage_vspk_interface import nuage_vspk_wrapper
import time

class ixchariot_webapi_wrapper():
    '''
    Initializations
    '''
    def __init__(self):
        self.webServerAddress = ixchariot_configuration.webServerAddress
        self.apiVersion = ixchariot_configuration.apiVersion
        self.username = ixchariot_configuration.username
        self.password = ixchariot_configuration.password
        self.apiKey = ixchariot_configuration.apiKey    
        
    def connect(self):
        print "Connecting to " + self.webServerAddress
        self.api = webApi.connect(self.webServerAddress, self.apiVersion, None, self.username, self.password)
        # It is also possible to connect with the API Key instead of username and password, using:
        #api = webApi.connect(webServerAddress, apiVersion, apiKey, None, None)
        
    def create_session(self):        
        try:
            session = self.api.createSession("ixchariot")
        except Exception, e:
            print("FAILED TO CONNECT TO IXIA CONSOLE")
            exit(1) 
                       
        print "Created session %s" % session.sessionId
        
        print "Starting the session..."
        session.startSession()
        print "CREATED NEW TEST SESSION"
        return session
    
    def get_session(self,session_id):        
        try:
            session = self.api.joinSession(int(session_id))
        except Exception, e:
            print("FAILED TO CONNECT TO EXISTING IXIA SESSION")
            exit(1) 
                       
        print "Joined session %s" % session.sessionId
        
        #print "Opening the session..."
        #session.startSession()
        print "JOINED EXISTING TEST SESSION"
        return session    
    
    def run_test(self,session_id,generate_zip):
        print("ENTERING session TEST RUN")
        
        session = self.get_session(session_id)
        result = session.startTest()
        
        seconds = 0
        while session.testIsRunning:
            time.sleep(1)
            seconds = seconds + 1
            print("Test is still running [" + str(seconds) + "s]")
             
        print("Test finished") 
        notifications = session.getErrorNotifications()
        
        for notification in notifications:
            print("[Debug] Notification: " + str(notification.message)) 
            
        # Get test level results.
        # Note: the statistic names should be identical to those that appear in the results CSV
        results = ixchariotApi.getTestLevelResults(session, ["Throughput"])    
        print("Aggregated Total Results:")
        min = 9000000000
        max = 0
        average = 0
        number_of_items = 0
        for res in results:
            # Each object in the list of results is of type Statistic (contains the statistic name and a list of StatisticValue objects).
            print(res.name)
            for val in res.values:
                # The list will contain StatisticValue objects for all the reported timestamps since the beginning of the test.
                # Each StatisticValue object contains the timestamp and the actual value.
                #print("time:" + str(val.timestamp) + "ms    " + str(val.value / 1048576) + "Mbps")
                if val.value > max :
                    max = val.value
                if val.value < min :
                    min = val.value
                average = average + val.value
                number_of_items = number_of_items + 1
            #print("")
            
        print("    MIN: " + str(min / 1048576) + "Mbps AVG:" + str(average / number_of_items / 1048576) + "Mbps MAX:" + str(max/ 1048576) + "Mbps")
        print("")    
        print('Generate_zip ? == ' + str(generate_zip))
        if generate_zip == 1:
            #Save all results to CSV files.
            print("SAVING RESULTS to zipped CSV files DUE json \generate-stats-zip\":\"yes\"")
            print("Saving the test results into zipped CSV files...\n")                
            filePath = time.strftime('%Y_%b_%d_%H_%M_%p_') + "_testResults.zip"
            print("Saving into " + filePath)
            with open(filePath, "wb+") as statsFile:
                self.api.getStatsCsvZipToFile(result.testId, statsFile)                
               
        # Get flow level results
        # Note: the statistic names should be identical to those that appear in the results CSV
        
        filterErrorMessage = "No statistics were reported for this test"
        (valuesList, query) = ixchariotApi.getRawResults(session, ["mix","Min Throughput", "Avg Throughput","Max Throughput"], None, filterErrorMessage)
        
        '''
        valuesList contains full filtered stats per timetick, so we will only use the last one
        '''
        results = valuesList[-1].values
        print("Flow / Min Throughput / Avg Throughput / Max Throughput")
        for result in results:
            if result[1] is None or result[1] is str or result[1] == "N/A":
                print("FLOW: " + result[0] + " - NO RESULTS - CONNECTION FAILED!")
            else:
                print("FLOW: " + result[0] + " [min/avg/max]: " + str(result[1] / 1048576) + "Mbps/" + str(result[2] / 1048576) + "Mbps/" + str(result[3] / 1048576) + "Mbps ["+ str(result[1]) + "bps/" + str(result[2]) + "bps/" + str(result[3]) + "bps]")            
    
        #import pdb; pdb.set_trace()
        
        '''
        print("FLOW STATISTICS: ")
        for flow in flow_names:
            results = ixchariotApi.getFlowLevelResults(session, ["Min Throughput", "Avg Throughput","Max Throughput"], flow, "TCP Baseline Performance", "TCP")
            if results[1].values[-1].value is str or results[1].values[-1].value == "N/A":
                print("FLOW: " + flow + " - NO RESULTS - CONNECTION FAILED!")
            else:
                print("FLOW: " + flow + " [min/avg/max]: " + str(results[0].values[-1].value / 1048576) + "Mbps/" + str(results[1].values[-1].value / 1048576) + "Mbps/" + str(results[2].values[-1].value / 1048576) + "Mbps ["+ str(results[0].values[-1].value) + "bps/" + str(results[1].values[-1].value) + "bps/" + str(results[2].values[-1].value) + "bps]")
        '''
            
    def connectivity_test(self,name,test_duration,delete_session_at_end,autostart,endpoints,stats_zip,optional_star_centers_array,optional_single_use_stars):
        print("ENTERING STAR connectivity TEST RUN")
        session = self.create_session()
        
        # FLOW NAMES 
        flow_names = []
        
        # Configure few test options
        testOptions = session.httpGet("config/ixchariot/testOptions")
        testOptions.testDuration = test_duration
        testOptions.runtimeErrorsToStopTest = 100
        testOptions.consoleManagementQoS = ixchariotApi.getQoSTemplateFromResourcesLibrary(session, "Best Effort")
        testOptions.endpointManagementQoS = ixchariotApi.getQoSTemplateFromResourcesLibrary(session, "Best Effort")
        session.httpPut("config/ixchariot/testOptions", data = testOptions) 
         
        # central 
        nuage = nuage_vspk_wrapper()
        nuage.connect() 
        
        for endpoint in endpoints:
            if endpoint['type'] == "nuage-vm"  and endpoint['endpoint-ip'] == "auto":
                endpoint['endpoint-ip'] = nuage.get_vport_for_enterprise_vm(endpoint['nuage-vm-enterprise'],
                                                                            endpoint['nuage-vm-domain'],
                                                                            endpoint['nuage-vm-zone'],
                                                                            endpoint['nuage-vm-subnet'],
                                                                            endpoint['nuage-vm-name']
                                                                            )
                if endpoint['endpoint-ip'] is None or endpoint['endpoint-ip'] == 'not-found': 
                    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                    print("XXX   ERROR! ERROR!  ERROR!    XXX")
                    print("XXX----------------------------XXX")
                    print("XXX One endpoint generator     XXX")
                    print("XXX doesn't have a correct IP! XXX")
                    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                    return 1;                                  
                
        iFlowID = 0;
        
        used = []

        ## HERE WE CREATE THE MESH
        for endpoint_SRC in endpoints:                                               
            for endpoint_DST in endpoints:
                
                print("")
                print("====================")
                print("Evaluating: "+ endpoint_SRC['endpoint-ip'] + "-to-" + endpoint_DST['endpoint-ip'])
                
                if optional_star_centers_array is not None and endpoint_DST['endpoint-ip'] not in optional_star_centers_array and endpoint_SRC['endpoint-ip'] not in optional_star_centers_array:
                    print("Breaking flow as optional-star-center defined, and not matched")
                    continue
                if optional_star_centers_array is not None and endpoint_DST['endpoint-ip'] in optional_star_centers_array and endpoint_SRC['endpoint-ip'] in optional_star_centers_array:
                    print("Both endpoints are from the same star center, removing ...")  
                    continue              
                
                            
                if endpoint_DST['endpoint-ip'] != endpoint_SRC['endpoint-ip']:
                    
                    if optional_single_use_stars and optional_single_use_stars == 'yes':
                        #OPTIONAL MAKE EVERY STAR CENTER USED ONLY ONCE 
                        if endpoint_DST['endpoint-ip'] in used:
                            print(endpoint_DST['endpoint-ip'] + " was already used, skipping.")
                            continue
                        if endpoint_SRC['endpoint-ip'] in used:
                            print(endpoint_SRC['endpoint-ip'] + " was already used, skipping.")
                            continue                       
                        used.append(endpoint_SRC['endpoint-ip'])
                        used.append(endpoint_DST['endpoint-ip'])
                    
                    #print("=====================================")
                    print("SRC "+endpoint_SRC['type']+" ip:" + endpoint_SRC['endpoint-ip'] + "[" + endpoint_SRC["ixia-management-ip"] + "]")                    
                    print("DST "+endpoint_DST['type']+" ip:" + endpoint_DST['endpoint-ip'] + "[" + endpoint_DST["ixia-management-ip"] + "]") 
                    
                    if endpoint_SRC['endpoint-ip'] == 'not-found' or endpoint_DST['endpoint-ip'] == 'not-found':
                        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                        print("XXX   ERROR! ERROR!  ERROR!    XXX")
                        print("XXX----------------------------XXX")
                        print("XXX One endpoint generator     XXX")
                        print("XXX doesn't have a correct IP! XXX")
                        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                        return 1;  
                    
                    '''
                    CREATION OF FLOW DEFINITION FOR THIS COMBINATION
                    '''
                    # Create a new FlowGroup
                    iFlowID = iFlowID + 1
                    name = endpoint_SRC['endpoint-ip'] + "-" + endpoint_DST['endpoint-ip']
                    flow_names.append(name)
                    print("FLOWGROUP creation: " + name)
                    direction = "SRC_TO_DEST"
                    topology = "FULL_MESH"
                    flowgroup = ixchariotApi.createFlowGroup(name, direction, topology)
                    
                    session.httpPost("config/ixchariot/flowGroups", data = flowgroup)
                    
                    session.httpPost("config/ixchariot/flowGroups/"+str(iFlowID)+"/network/sourceEndpoints", 
                                     data = ixchariotApi.createEndpoint(
                                         endpoint_SRC['endpoint-ip'], 
                                         endpoint_SRC["ixia-management-ip"]))
                    session.httpPost("config/ixchariot/flowGroups/"+str(iFlowID)+"/network/destinationEndpoints", 
                                     data = ixchariotApi.createEndpoint(
                                         endpoint_DST['endpoint-ip'], 
                                         endpoint_DST["ixia-management-ip"])) 
                    
                    flowList = [
                                    # Data flows
                                    ["TCP Baseline Performance",     1,          "TCP",      "None",    "None"]
                                    #["UDP Baseline Performance",     1,          "UDP",      "None",    "None"]
                                    #["UDP Low Performance",     1,          "UDP",      "None",    "None"]
                                    #["TCP Baseline Performance",     1,          "TCP",      "Best Effort",    "Background"]
                                    #["UDP Baseline Performance",    3,          "UDP",      "Background",    "None"],
                                
                                    # VoIP flows
                                    #["G.711a (64 kbps)",             1,          "RTP",      "Voice",        "None"],
                                
                                    # Video over RTP flows
                                    #["RTP HD (10 Mbps)",            1,         "RTP",     "Audio Video",    "None"],
                                    
                                    # Adaptive video over HTTP flows
                                    #["Netflix Video SD",            1,         "TCP",     "None",            "None"]
                                ]

                    for i in range (0, len(flowList)):
                        flowData = flowList[i]
                        flowName = flowData[0]
                        users = flowData[1]
                        protocol = flowData[2]
                        sourceQoSName = flowData[3]
                        destinationQoSName = flowData[4]
                        flowScript = ixchariotApi.getFlowScriptFromResourcesLibrary(session, flowName)
                    
                        # TH   IS IS NECESSARY TO WORK WITH VTEPS
                        #ixchariotApi.changeFlowScriptParameterValue(flowScript, "MSS", "1410")
                        #ixchariotApi.changeFlowScriptParameterValue(flowScript, "Send Buffer Size", "1300")
                        #ixchariotApi.changeFlowScriptParameterValue(flowScript, "Receive Buffer Size", "1300")
                        # Example for changing the parameter values
                        #if i == 3:
                        #    ixchariotApi.changeFlowScriptParameterValue(flowScript, "Bit Rate", "9.8 Mbps")
                        
                        #if i == 4:
                        #    ixchariotApi.changeFlowScriptParameterValue(flowScript, "Segment Duration (s)", "3")
                            
                        sourceQoSTemplate = ixchariotApi.getQoSTemplateFromResourcesLibrary(session, sourceQoSName)
                        destinationQoSTemplate = ixchariotApi.getQoSTemplateFromResourcesLibrary(session, destinationQoSName)
                        
                        flow = ixchariotApi.createFlow(flowScript, users, protocol, sourceQoSTemplate, destinationQoSTemplate)
                        session.httpPost("config/ixchariot/flowGroups/"+str(iFlowID)+"/settings/flows", data = flow)                    
                    
        
        
        if autostart == "yes":
            
            print("")
            print("EXECUTING TEST VIA json AUTOSTART=\"yes\"")
            
            if stats_zip == "yes":
                self.run_test(session.sessionId, 1)
            else:
                self.run_test(session.sessionId, 0)


        if delete_session_at_end == "yes":
            session.stopSession()
            print("SESSION " +str(session.sessionId)+ " DELETION DUE json \"delete-session-at-end\":\"yes\"")
            session.httpDelete()            

        

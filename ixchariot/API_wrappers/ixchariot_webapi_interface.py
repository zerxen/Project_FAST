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
    
    def connectivity_mesh_test(self,name,test_duration,delete_session_at_end,autostart,endpoints,stats_zip):
        print("ENTERING basic_connectivity_test TEST RUN")
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
                
        iFlowID = 0;

        ## HERE WE CREATE THE MESH
        for endpoint_SRC in endpoints:                                               
            for endpoint_DST in endpoints:
                if endpoint_DST['endpoint-ip'] != endpoint_SRC['endpoint-ip']:
                    print("=====================================")
                    print("SRC "+endpoint_SRC['type']+" ip:" + endpoint_SRC['endpoint-ip'] + "[" + endpoint_SRC["ixia-management-ip"] + "]")                    
                    print("DST "+endpoint_DST['type']+" ip:" + endpoint_DST['endpoint-ip'] + "[" + endpoint_DST["ixia-management-ip"] + "]") 
                    
                    '''
                    CREATION OF FLOW DEFINITION FOR THIS COMBINATION
                    '''
                    # Create a new FlowGroup
                    iFlowID = iFlowID + 1
                    name = "S:" + endpoint_SRC['endpoint-ip'] + " D:" + endpoint_DST['endpoint-ip']
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
                                    ["TCP Baseline Performance",     1,          "TCP",      "Best Effort",    "Background"]
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
                    
                        # THIS IS NECESSARY TO WORK WITH VTEPS
                        ixchariotApi.changeFlowScriptParameterValue(flowScript, "MSS", "1410")
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

            '''
            try:
                print "Starting the test..."
                results = session.runTest()
                
            except Exception, e:
                if 'The error was detected at runtime.' in str(e):
                    print("DEBUG: There was a runtime problem, can be a simple endpoint pairs not able to communicate, check results for 0 performance combinations")
                else:
                    print("ERROR: THERE WAS A PROBLEM RUNNING THE TEST, EXITING")
                    print "Error", e 
                    exit(1)
                 
            '''    
            

            
            #time.ctime() # 'Mon Oct 18 13:35:29 2010'
            #time.strftime('%l:%M%p %Z on %b %d, %Y') # ' 1:36PM EDT on Oct 18, 2010'
            #time.strftime('%l:%M%p %z on %b %d, %Y') # ' 1:36PM EST on Oct 18, 2010' 
            
            if stats_zip == "yes":
                #Save all results to CSV files.
                print("SAVING RESULTS to zipped CSV files DUE json \generate-stats-zip\":\"yes\"")
                print("Saving the test results into zipped CSV files...\n")                
                filePath = time.strftime('%Y_%b_%d_%H_%M_%p_') + "_testResults.zip"
                print("Saving into " + filePath)
                with open(filePath, "wb+") as statsFile:
                    self.api.getStatsCsvZipToFile(result.testId, statsFile)
                #self.api.getStatsCsvZipToFile(session.sessionId, statsFile)
                    
                
            # Get results after test run.
            # The functions below can also be used while the test is running, by using session.startTest() to start the execution,
            # calling any of the results retrieval functions during the run, and using session.waitTestStopped() to wait for test end.
            # You can use time.sleep() to call the results retrieval functions from time to time.
            # These functions will return statistics for all the timestamps reported since the beginning of the test until the current moment.
            results = ixchariotApi.getTestLevelResults(session, ["Throughput"])
            
            # Get test level results.
            # Note: the statistic names should be identical to those that appear in the results CSV
            
            print "Aggregated Total Results: \n"
            for res in results:
                # Each object in the list of results is of type Statistic (contains the statistic name and a list of StatisticValue objects).
                print(res.name)
                for val in res.values:
                    # The list will contain StatisticValue objects for all the reported timestamps since the beginning of the test.
                    # Each StatisticValue object contains the timestamp and the actual value.
                    print("time:" + str(val.timestamp) + "ms    " + str(val.value / 1048576) + "Mbps")
                print("")
               
            # Get flow level results
            # Note: the statistic names should be identical to those that appear in the results CSV
            print("FLOW STATISTICS: ")
            for flow in flow_names:
                results = ixchariotApi.getFlowLevelResults(session, ["Min Throughput", "Avg Throughput","Max Throughput"], flow, "TCP Baseline Performance", "TCP")
                if results[1].values[-1].value is str or results[1].values[-1].value == "N/A":
                    print("FLOW: " + flow + " - NO RESULTS - CONNECTION FAILED!")
                else:
                    print("FLOW: " + flow + " [min/avg/max]: " + str(results[0].values[-1].value / 1048576) + "Mbps/" + str(results[1].values[-1].value / 1048576) + "Mbps/" + str(results[2].values[-1].value / 1048576) + "Mbps ["+ str(results[0].values[-1].value) + "bps/" + str(results[1].values[-1].value) + "bps/" + str(results[2].values[-1].value) + "bps]")
                
                #for res in results:
                #    print res.name
                #    print res.values[-1].timestamp
                #    print res.values[-1].value
                #    print ""                

            
              
        
        if delete_session_at_end == "yes":
            session.stopSession()
            print("SESSION " +str(session.sessionId)+ " DELETION DUE json \"delete-session-at-end\":\"yes\"")
            session.httpDelete()

        

import json
from pprint import pprint
from ixchariot.API_wrappers.ixchariot_webapi_interface import ixchariot_webapi_wrapper
from nuage.API_wrappers.nuage_vspk_interface import nuage_vspk_wrapper

def ixchariot_load_json(args):
    #pprint (args)
    
    #pprint(args.INFILE)
    print("Loading: " + str(args.INFILE))
    data = json.load(args.INFILE)
    args.INFILE.close()
    
    ''' SILENT '''
    bSilent = False;
    if args.silent == 0:
        print("##########")
        print("non-silent");
        print("##########")
    else:
        bSilent = True;

    if bSilent == False:
        try:
            for test in data['tests']:
                print("")
                print("TEST: " + test['name'])
                print("    type:" + test['type'])
                if test.get('optional-star-centers',None) is not None:
                    for star in test['optional-star-centers']:
                        print("    star node:" + star)
                print("    optional-sigle-use-stars: " + test.get('optional-single-use-stars','no'))
                print("    optional-stars-unidirectional: " + test.get('optional-stars-unidirectional','any'))
                print("    optional-traffic-ixia-flow: "   + test.get('optional-traffic-ixia-flow','TCP Baseline Performance'))
                print("    optional-traffic-ixia-protocol: " + test.get('optional-traffic-ixia-protocol','TCP'))            
                print("    endpoint-types:" + test['endpoint-types'])
                print("    delete session at the end?:" + test['delete-session-at-end'])
                print("    generate stats zip?:" + test['generate-stats-zip'])
                print("    autostart: " + test['autostart'])
                print("    test-duration: " + test['test-duration'])
                for endpoint in test['endpoints']:
                    print("    ENDPOINT type:" + endpoint['type'])
                    if endpoint['type'] == "static":
                        print("        ixia-management-ip: " + endpoint['ixia-management-ip'])
                        print("        endpoint-ip: " + endpoint['endpoint-ip'])
                    
                    if endpoint['type'] == "nuage-vm":
                        print("        ixia-management-ip: " + endpoint['ixia-management-ip'])
                        print("        nuage-vm-name: " + endpoint['nuage-vm-name'])
                        print("        nuage-vm-enterprise "+ endpoint['nuage-vm-enterprise'])
                        print("        nuage-vm-domain "+ endpoint['nuage-vm-domain'])
                        print("        nuage-vm-zone "+ endpoint['nuage-vm-zone'])
                        print("        nuage-vm-subnet " + endpoint['nuage-vm-subnet'])         
    
        except Exception, e:
            print('Caught exception: %s' % str(e))
            return 1   
    
        print("")
        print("Looks like the JSON go loaded completely, will create test runs now...")
    
    ixchariot = ixchariot_webapi_wrapper()
    ixchariot.connect()
    print("Connected, executing test...")
    
    for test in data['tests']:
        if test['type'] == 'connectivity-test' and test['endpoint-types'] == 'explicit':
            ixchariot.connectivity_test(test['name'],test['test-duration'],test['delete-session-at-end'],
                                        test['autostart'],test['endpoints'],test['generate-stats-zip'],
                                        test.get('optional-star-centers',None),test.get('optional-single-use-stars',False),
                                        test.get('optional-stars-unidirectional','any'),
                                        test.get('optional-traffic-ixia-flow','TCP Baseline Performance'),
                                        test.get('optional-traffic-ixia-protocol','TCP'),
                                        bSilent
                                        )
        else:
            print("Unknown test type, skipping.")
        
            
            
 
    
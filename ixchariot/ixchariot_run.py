import json
from pprint import pprint
from ixchariot.API_wrappers.ixchariot_webapi_interface import ixchariot_webapi_wrapper

def ixchariot_run(args):
    pprint (args)
    
    if args.OBJECT is None:
        print("ixchariot run didn't recieved mandatory parameter, exiting ....")
        return
    
    if args.OBJECT == 'session':
        print("show users starting ...")
        if args.id is None or args.id == '':
            print("You didn't specified session ID with --id")
            return 1
         
        
        ixchariot = ixchariot_webapi_wrapper()
        ixchariot.connect()       
        
        ixchariot.run_test(args.id[0],args.generate_zip) 
        return 0
    
    

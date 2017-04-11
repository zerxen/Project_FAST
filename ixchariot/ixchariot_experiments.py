import json
from pprint import pprint
from ixchariot.webapi.ixchariot_sample import test01
from nuage.API_wrappers.nuage_vspk_interface import nuage_vspk_wrapper

def ixchariot_experiments(args):
    pprint (args)
    
    if args.OBJECT is None:
        print("ixchariot experiments didn't recieved mandatory parameter, exiting ....")
        return
    
    if args.OBJECT == 'test01':
        print("test01 show users starting ...")
        test01()
        return
    
    

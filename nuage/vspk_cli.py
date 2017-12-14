'''
Created on Dec 14, 2017

@author: havrila
'''

from pprint import pprint
from nuage.API_wrappers.nuage_vspk_interface import nuage_vspk_wrapper

def nuage_vspk_cli(args):
    pprint (args)

    nuage = nuage_vspk_wrapper();
    nuage.connect()      
    nuage.debug_cli()
        
    return 0

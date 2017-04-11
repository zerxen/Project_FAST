from pprint import pprint
def fortinet_show(args):
    pprint (args)
    
    if args.OBJECT is None:
        print("fortinet show didn't recieved mandatory parameter, exiting ....")
        return 
    
    if args.OBJECT == 'interfaces':
        print("fortinet interfaces starting ...")

        print("")
        print("===========")
        print("UNSUPPORTED")
        print("===========")
        print("Unfortunatelly this version of FAST doesn't yet support Fortinet systems")
        #if args.management_ip is None or args.management_ip == '':
        #    print ("DEBIL zadaj managemetn IP")
        #else:
        #    print ("Jeee, mam management IP " + args.management_ip[0])     
    
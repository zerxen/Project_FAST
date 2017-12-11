# Project FAST

Is a Nuage/vmWare/IxChariot API aggregation and CLI tool, with target 
to help you control these systems in a more linux like and scriptable 
way for longer and more complex test runs (my original motivation was 
to have this tool execute long test scenarios one-by-one in 
pre-production tests to avoid shitload of GUI clicking) 
```
                           ..   ..  ..  .... ..                               
                      ,7MMMMMMMMMMMMMMMMMMMMMMMMMN7,                          
                 IMMMMS...MMMMMMMMMMMMMMMMM+..,,,,,,,MMMS.                    
            ..+MMMMMMMM,,,,,,,MMMMMMMMMMMMMM:,,,,: ..,MMMMMM.                 
            MMMMMMMMMMMMMMM.,,,,..,,MMMM,,,,,,:MMMMMMMMMMMMMMM                
           MMMMMMMMMMMMMMMNMMMMMMMMMMMMMM MMMMMMMMMMMMMMMMMMMMM               
           NMMMMMMMMMMMMMMMMMMM8,.MMMMMMMMMMMMMMMMMMMMMMMMMMMMZ               
M           NMMMMMMMMMMMMMMM8,,,,,,MMMM,,,,,,,,MMMMMMMMMMMMMMZM            M  
SM          NMMMMMMMM,.....,,,,MMMMMMMMMMMMMMM.,,,,,7MMMMMMMMMMM           M,  
.MM.        NMMMMMMZMMI,,,,,,,.,MMMMMMMMMMMMMMMMM8.,. MMZMMMMMMM         .MM   
:MMM       NMMMMMMMMMMMMMZMMMMMMMMMMMMMMMMMMMMMM7MMMMMMMMMMMMMM        MM    
 MMMM.     NMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM       MMMM    
  MMMMZ.   NMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM     .MMMM.    
   MMMMM  .NMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM   .+MMMM      
   .MMMMM  .MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM.  .NMMMM.      
     MMMMMM  :MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM.   MMMMM        
      MMMMMM+   ~MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM.   .MMMMMM         
       MMMMMMM.      MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM.       :MMMMMM          
         MMMMMMN        . .. . ,NMNNNNNNNM.,. .. .         :MMMMMMM.          
          MMMMMMMN                                       ZMMMMMMM.            
           IMMMMMMMM.                                  OMMMMMMMZ              
            .MMMMMMMMM                               MMMMMMMMM.               
               MMMMMMMMM                          .MMMMMMMMM.                 
                 MMMMM.MMM                      ,MMMMMMMMM.                   
                  ~MMMMM.MMM:.                NMM8 MMMMM                      
                    ,MMMMO.MMMM.           +MMM. MMMMM                        
           .          .MMMMM..MMMN.   ..MMMM. IMMMMM                          
          .MMMM          ~MMMMM .MMMM...M.. MMMMM          . .                
            MMM.            MMMMMM..MMMMM  .MM+..         =MMMM               
            .7MM         +MMM .MMMMMM. ~MMMMMI           .MMM                 
   .  .       MMM ~MMMMMMMMM.. .=.+NMMMMM  MMMMMMM. .   MMM                  
   MMMMMMMMM+.MMMM .+I .  MMMMMMMM ..MMMMMMM  SMMMMMM:.MMM                   
   MMMM MMMMMMM  MMM  MMMMMMM  .         DMMMMMM    SMMMM ,MMMMMM.MMM        
   .MMM. ..     .MMM  ..                       .,MMM. MMM MMMMMMMMMMM.       
       M         MMM .                                MM,       ..MMMM        
                 .MMMM .Z.                           MMM         MM           
                    MMMMMM                     MMMMMMMM                       
                                                OMMM
```                                                               
## (c) Peter Havrila
This software is sponsored by [NetworkGeekStuff.com](http://networkgeekstuff.com/)
phavrila@gmail.com

Please read README.TXT to know how to configure this software before running it 
against your Nuage/vmware/ixchariot as access parameters to these systems are 
taken from these files, not as arguments

Hint: Always explore -h in each level of nested commandline

## DEPENDENCIES:
1) Python 2.7 (unfortunatelly incompatible with Python 3.x)
2) pip2 install vspk
3) pip2 install pyvmomi ipaddress
             

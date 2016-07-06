""" Kondo RCB-1 Serial Port Module

Kondo Robot Control Board (RCB-1) generic serial command/response interface.

Author:	Robin D. Knight
Email:	robin.knight@radnarrowsrobotics.com
URL:	http://www.roadnarrowsrobotics.com
Date:	2005.10.26

Copyright (C) 2005.  RoadNarrows LLC.
"""

def binToHexStr( binData ):
    """ Convert binary data to readable ascii hex string.

	Parameters:
	    binData - string or list of binary data bytes

	Return Value:
	    Ascii hex string format: '0xhh 0xhh 0xhh ... 0xhh '
    """
    if type(binData) is list:
	f = lambda x: x
    else:
	f = lambda x: ord(x)
    s = ''

    for b in binData:
	s += "0x%02x " % f(b)
    return s

""" ==========================
	Test
    ==========================
"""
list = [10, 20]
print binToHexStr(list)



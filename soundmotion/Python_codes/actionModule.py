""" --------------------------------------------------
    actionModule

    Function:
    - read inputs from interaction
    - selects motions
    - adjust motion parameters
    - return motion to be executed
    --------------------------------------------------
"""

import glob
import KHR1readcsv as motion
import KHR1_motionrange2 as khr1range
import re


class actionModule:

    def __init__(self):
        pass

    def rule(self, action, mood, heartrate):
        hello = re.compile('hello', re.IGNORECASE)
        bye = re.compile('^(bye|goodbye)|(bye|goodbye)*$', re.IGNORECASE)
def retest3(word):
	bye = re.compile('^(bye|goodbye)|(bye|goodbye)$', re.IGNORECASE)
	p = bye.search(word)
	print p
	if p:
		print p.group()
	else:
		print 'no p'

>>> retest('hello')
<_sre.SRE_Match object at 0xa473d40>
hello
>>> retest3('hello')
None
no p
>>> retest3('goodbye for now')
<_sre.SRE_Match object at 0xa52e2a8>
goodbye
>>> retest3('well, i guess this is goodbye')
<_sre.SRE_Match object at 0xa52e0f8>
goodbye
>>> retest3('well, goodbye ole')
None
no p

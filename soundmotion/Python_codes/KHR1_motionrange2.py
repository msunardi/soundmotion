""" ========================
    Key naming conventions:
	- Joint Axis {X,Y,Z}:
	    - X: pointing forward/back (i.e. front/back)
	    - Y: to sides (i.e. left/right)
	    - Z: pointing up/down 

	- DOFs (joints) keys/labels:
	    <side><joint><axis/direction>
	    e.g.: 'LShoulderX'
	    mean: Left-Shoulder-X(axis) (i.e. Channel 2 on KHR-1)
	
	- Dictionary entry:
	    <key>: [ <channel #>, <min_range>, <max_range>, <home_position> ]
	    e.g.: 'LShoulderX': [2, 0, 180, 0]
	    mean: Left-Shoulder-X(axis), Channel #: 2, minimum range*: 0, maximum range**: 180, home position: 0

	*"minimum range" is perceived as motion range towards center of body (inwards) or ground (downwards) or rear (backwards).  FOr Head, it's left
	**"maximum range" : motion range away from the center of body (outwards and upwards), or front (forward).  For Head, it's right
"""

KHR1motionrange = {
    'LShoulderY': [1, 0, 180, 0], 'LShoulderX': [2, 0, 180, 0],
    'LElbowX': [3, 0, 180, 90],
    'HeadZ': [6, 0, 180, 90],
    'RShoulderY': [7, 180, 0, 180], 'RShoulderX': [8, 180, 0, 180],
    'RElbowX': [9, 180, 0, 90],
    'LHipX': [13, 0, 99, 90], 'LHipY': [14, 0, 180, 129],
    'LKneeY': [15, 0, 180, 125],
    'LAnkleY': [16, 0, 180, 90], 'LAnkleX': [17, 180, 32, 90],
    'RHipX': [19, 81, 180, 90], 'RHipY': [20, 180, 0, 51],
    'RKneeY': [21, 180, 0, 55],
    'RAnkleY': [22, 180, 0, 90], 'RAnkleX': [23, 0, 180, 90]}

KHR1motionrange2 = {
    0: ['LShoulderY', 0, 180, 0],
    1: ['LShoulderX', 0, 180, 0],
    2: ['LElbowX', 0, 180, 90],
    3: ['N/A', 225, 225, 225],
    4: ['N/A', 225, 225, 225],
    5: ['HeadX', 0, 180, 90],
    6: ['RShoulderY', 180, 0, 180],
    7: ['RShoulderX', 180, 0, 180],
    8: ['RElbowX', 180, 0, 90],
    9: ['N/A', 225, 225, 225],
    10: ['N/A', 225, 225, 225],
    11: ['N/A', 225, 225, 225],
    12: ['LHipX', 0, 99, 90],
    13: ['LHipY', 0, 180, 129],
    14: ['LKneeY', 0, 180, 125],
    15: ['LAnkleY', 0, 180, 90],
    16: ['LAnkleX', 180, 32, 90],
    17: ['N/A', 225, 225, 225],
    18: ['RHipX', 81, 180, 90],
    19: ['RHipY', 180, 0, 51],
    20: ['RKneeY', 180, 0, 55],
    21: ['RAnkleY', 180, 0, 90],
    22: ['RAnkleX', 0, 180, 90],
    23: ['N/A', 225, 225, 225]}

"""mr = KHR1motionrange2.keys()
mr.sort()

for k, v in KHR1motionrange2.iteritems():
    print k, v[0], v[1], v[2], v[3]
"""

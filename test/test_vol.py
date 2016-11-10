import subprocess
from ceilometer.compute.vmi.volatility import  VolInspector

def testVolInspector():
    instance_name = "instance-00000014"
    inspector=VolInspector()
    plist = inspector.get_process_list(instance_name)
    print(plist)

testVolInspector()
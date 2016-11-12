import subprocess
from ceilometer.compute.vmi.volatility import  VolInspector

def testVolInspector():
    instance_name = "instance-00000014"
    inspector=VolInspector()
    process_list = inspector.get_process_list(instance_name)
    print(len(process_list))

testVolInspector()
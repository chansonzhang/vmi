import subprocess
from ceilometer.compute.vmi.model import Process

class VolInspector(object):

    '''
    Offset             Name                 Pid             Uid             Gid    DTB                Start Time
    ------------------ -------------------- --------------- --------------- ------ ------------------ ----------
0   xffff88003da30000 systemd              1               0               0      0x000000003d63d000 2016-11-01 06:52:13 UTC+0000
    '''
    def get_process_list(self,instance_name):
        command="vol.py -l vmi://"+instance_name+" --profile LinuxCentos7-3_10_0-327_36_3_el7_x86_64x64 linux_pslist"
        out = subprocess.check_output(command, shell=True).decode('utf-8')
        raw_list = out.split("\n")
        process_list = [];
        for index in range(len(raw_list)):
            if(index>=2): #jump the header and seperator line
                elements = raw_list[index].split(" ")
                process = Process(elements[1],elements[2],elements[3],elements[4],elements[6],elements[5],elements[0])
                process_list.append(process)
        return process
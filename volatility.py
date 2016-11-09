import subprocess

class VolInspector(object):

    def get_process_list(self,instance_name):
        command="vol.py -l vmi://"+instance_name+" --profile LinuxCentos7-3_10_0-327_36_3_el7_x86_64x64 linux_pslist"
        out = subprocess.call(command, shell=True)
        return out
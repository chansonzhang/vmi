# @Time    : 2016/11/10 12:01
# @Author  : Zhang Chen
# @Email    : zhangchen.shaanxi@gmail.com
from oslo_log import log
import subprocess
from ceilometer.compute.vmi.model import Process

LOG = log.getLogger(__name__)


class VolInspector(object):
    def check_sanity(self):
        """Check the sanity of hypervisor inspector.

        Each subclass could overwrite it to throw any exception
        when detecting mis-configured inspector
        """
        pass

    '''
    Offset             Name                 Pid             Uid             Gid    DTB                Start Time
    ------------------ -------------------- --------------- --------------- ------ ------------------ ----------
0   xffff88003da30000 systemd              1               0               0      0x000000003d63d000 2016-11-01 06:52:13 UTC+0000
    '''

    def get_process_list(self, instance_name):
        command = "vol.py -l vmi://" + instance_name + " --profile LinuxCentos7-3_10_0-327_36_3_el7_x86_64x64 linux_pslist"
        out = subprocess.check_output(command, shell=True).decode('utf-8')
        raw_list = out.split("\n")
        process_list = []
        for index in range(len(raw_list)):
            if (index >= 2):  # jump the header and seperator line
                elements = raw_list[index].split()
                if (len(elements) < 9):
                    continue
                try:
                    process = Process(elements[1], elements[2], elements[3], elements[4],
                                      elements[6] + " " + elements[7] + " " + elements[8], elements[5], elements[0])
                except subprocess.CalledProcessError as e:
                    out_bytes = e.output  # Output generated before error
                    code = e.returncode  # Return code
                    LOG.error(
                        "Error when get process, the output generated before error:%(out_bytes)s, the return code is %(return_code)s",
                        {'out_bytes': out_bytes,
                         'return_code': code})
                process_list.append(process)
        return process_list

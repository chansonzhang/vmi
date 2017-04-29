# @Time    : 2017/4/28 21:22
# @Author  : Zhang Chen
# @Email    : zhangchen.shaanxi@gmail.com
# @File    : fileUtils.py
import os
import time;
from oslo_log import log
LOG = log.getLogger(__name__)

class FileUtils:
    data_dir = "/experiment/"
    file_prefix = time.strftime("%Y%m%d%H0000-", time.localtime())
    file_name = "introspection_latency";

    @classmethod
    def write_introspection_latency(cls,content):
        if os.path.isdir(cls.data_dir):
            pass;
        else:
            os.mkdir(cls.data_dir,0o777);

        LOG.debug('Using dir %s', os.path.abspath(cls.data_dir))
        file = open(cls.data_dir + cls.file_prefix + cls.file_name,'a');
        file.write(str(content)+"\n")
        file.close();



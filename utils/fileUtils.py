# @Time    : 2017/4/28 21:22
# @Author  : Zhang Chen
# @Email    : zhangchen.shaanxi@gmail.com
# @File    : fileUtils.py
import time;

class FileUtils:
    data_dir = "./data/"
    file_prefix = time.strftime("%Y%m%d%H0000-", time.localtime())
    file_name = "introspection_latency";

    @classmethod
    def write_introspection_latency(cls,content):
        file = open(cls.data_dir + cls.file_prefix + cls.file_name,'a');
        file.write(content+"\n")
        file.close();



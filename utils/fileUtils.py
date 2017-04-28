# @Time    : 2017/4/28 21:22
# @Author  : Zhang Chen
# @Email    : zhangchen.shaanxi@gmail.com
# @File    : fileUtils.py
import time;

class FileUtils:
    data_dir = "./data/"
    file_prefix = time.strftime("%Y%m%d%H0000-", time.localtime())
    file_name = "introspection_latency";

    @staticmethod
    def write_introspection_latency(self, content):
        file = open(self.data_dir + self.file_prefix + self.file_name,'a');
        file.write(content+"\n")
        file.close();



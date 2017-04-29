# @Time    : 2017/4/28 22:25
# @Author  : Zhang Chen
# @Email    : zhangchen.shaanxi@gmail.com
# @File    : testFileUitls.py.py
from ceilometer.compute.vmi.utils.fileUtils import FileUtils;
import datetime;
import time;

def testFileUtils():
    time1 = datetime.datetime.now();
    time.sleep(1);
    time2 = datetime.datetime.now();
    latency = (time2 - time1).seconds;
    FileUtils.write_introspection_latency(latency);

testFileUtils()
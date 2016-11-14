# @Time    : 2016/11/10 12:01
# @Author  : Zhang Chen
# @Email    : zhangchen.shaanxi@gmail.com
from oslo_log import log
import subprocess
import pika
import uuid
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
        vmi_rpc = VMIRpcClient()
        LOG.debug(" [x] Requesting get_process_list(%s)", instance_name)
        raw_list = vmi_rpc.call(instance_name)
        LOG.debug(" [.] Got %s" % raw_list)
        process_list = []
        LOG.debug("Length of raw_list: %s" % len(raw_list))
        for index in range(len(raw_list)):
            if (index >= 2):  # jump the header and seperator line
                elements = raw_list[index].split()
                if (len(elements) < 9):
                    continue
                process = Process(elements[1], elements[2], elements[3], elements[4],
                                      elements[6] + " " + elements[7] + " " + elements[8], elements[5], elements[0])
                process_list.append(process)
        LOG.debug('Instance: %(instance_name)s, Length: %(length)s',
                  {'instance_name': instance_name,
                   'length': len(process_list)})
        return process_list


class VMIRpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, instance_name):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=str(instance_name))
        while self.response is None:
            self.connection.process_data_events()
        return str(self.response)


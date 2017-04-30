# @Time    : 2016/11/10 12:01
# @Author  : Zhang Chen
# @Email    : zhangchen.shaanxi@gmail.com
# @File    : process.py

from oslo_config import cfg
from oslo_log import log
LOG = log.getLogger(__name__)
import ceilometer
import datetime;
from ceilometer import sample
from ceilometer.i18n import _, _LE, _LW
from ceilometer.agent import plugin_base
from ceilometer.compute import pollsters
from ceilometer.compute.pollsters import util
from ceilometer.compute.vmi import inspector as vmi_inspector
from ceilometer.compute.vmi.volatility import VolInspector
from ceilometer.compute.vmi.utils.fileUtils import FileUtils;



class ProcessListPollster(pollsters.BaseComputePollster):
    @property
    def inspector(self):
        try:
            inspector = ProcessListPollster._vol_inspector
        except AttributeError:
            inspector = VolInspector()
            ProcessListPollster._vol_inspector = inspector
        return inspector

    def get_samples(self, manager, cache, resources):
        self._inspection_duration = self._record_poll_time()
        for instance in resources:
            state = instance.status.lower()
            if (state != 'active'):
                LOG.info("Skip the instance with status %(instance_state)s", {'instance_state': state})
                continue
            instance_name = util.instance_name(instance)
            LOG.debug('Getting process list for instance %s', instance_name)
            try:
                LOG.debug('Using inspector %s', self.inspector)
                time1=datetime.datetime.now();
                process_list = self.inspector.get_process_list(instance_name)
                time2=datetime.datetime.now();
                latency=(time2-time1).total_seconds();
                timestamp = time1.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                FileUtils.write_introspection_latency(timestamp+"\t"+(str)(latency*1000));
                LOG.debug("PROCESS LIST: %(instance)s lenth: %(plist_length)s",
                          {'instance': instance,
                           'plist_length': process_list[0]['process_name']})
                yield util.make_sample_from_instance(
                    instance,
                    name='instance.process.list',
                    type=sample.TYPE_GAUGE,
                    unit='instance',
                    volume=process_list,
                )
            except vmi_inspector.InstanceNotFoundException as err:
                # Instance was deleted while getting samples. Ignore it.
                LOG.debug('Exception while getting samples %s', err)
            except vmi_inspector.InstanceShutOffException as e:
                LOG.debug('Instance %(instance_id)s was shut off while '
                          'getting samples of %(pollster)s: %(exc)s',
                          {'instance_id': instance.id,
                           'pollster': self.__class__.__name__, 'exc': e})
            except vmi_inspector.InstanceNoDataException as e:
                LOG.warning(_LW('Cannot inspect data of %(pollster)s for '
                                '%(instance_id)s, non-fatal reason: %(exc)s'),
                            {'pollster': self.__class__.__name__,
                             'instance_id': instance.id, 'exc': e})
            except vmi_inspector.NoDataException as e:
                LOG.warning(_LW('Cannot inspect data of %(pollster)s for '
                                '%(instance_id)s: %(exc)s'),
                            {'pollster': self.__class__.__name__,
                             'instance_id': instance.id, 'exc': e})
                raise plugin_base.PollsterPermanentError(resources)
            except ceilometer.NotImplementedError:
                # Selected inspector does not implement this pollster.
                LOG.debug('Obtaining Memory Usage is not implemented for %s',
                          self.inspector.__class__.__name__)
                raise plugin_base.PollsterPermanentError(resources)
            except Exception as err:
                LOG.exception(_('Could not get Process List for '
                                '%(id)s: %(e)s'), {'id': instance.id,
                                                   'e': err})


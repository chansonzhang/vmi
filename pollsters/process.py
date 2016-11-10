#
# Copyright 2012 eNovance <licensing@enovance.com>
# Copyright 2012 Red Hat, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from oslo_config import cfg
from oslo_log import log

import  ceilometer
from ceilometer import sample
from ceilometer.i18n import _, _LE, _LW
from ceilometer.agent import plugin_base
from ceilometer.compute import pollsters
from ceilometer.compute.pollsters import util
from ceilometer.compute.vmi import inspector as vmi_inspector
from ceilometer.compute.vmi.volatility import VolInspector
LOG = log.getLogger(__name__)

class ProcessListPollster(pollsters.BaseComputePollster):

    def inspector(self):
        try:
            inspector = self._inspector
        except AttributeError:
            inspector = VolInspector()
            self._inspector = inspector
        return inspector

    def get_samples(self, manager, cache, resources):
        self._inspection_duration = self._record_poll_time()
        for instance in resources:
            instance_name=util.instance_name(instance)
            LOG.debug('Getting process list for instance %s',instance_name )
            try:
                process_list = self.inspector.get_process_list(instance_name)
                LOG.debug("PROCESS LIST: %(instance)s lenth: %(plist_length)f",
                          {'instance': instance,
                           'plist_length': len(process_list)})
                yield util.make_sample_from_instance(
                    cfg.CONF,
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
                LOG.exception(_('Could not get Memory Usage for '
                                '%(id)s: %(e)s'), {'id': instance.id,
                                                   'e': err})
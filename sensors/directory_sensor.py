import os

from st2reactor.sensor.base import PollingSensor


class DirectorySensor(PollingSensor):
    def setup(self):
        self._logger = self._sensor_service.get_logger(__name__)

        # initialize directory info
        self._cached_dirinfo = self._get_dirinfo()

    def poll(self):
        current_dirinfo = self._get_dirinfo()

        # notify deleted files
        for path in (set(self._cached_dirinfo) - set(current_dirinfo)):
            self._dispatch_trigger(path, self._cached_dirinfo[path], 'deleted')

        # notify created files
        for path in (set(current_dirinfo) - set(self._cached_dirinfo)):
            self._dispatch_trigger(path, current_dirinfo[path], 'created')

        # notify modified files
        for path in [x for x in (set(self._cached_dirinfo) & set(current_dirinfo))
                             if self._cached_dirinfo[x] != current_dirinfo[x]]:
            self._dispatch_trigger(path, current_dirinfo[path], 'modified')

        # update cache data
        self._cached_dirinfo = current_dirinfo

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def _get_created_files(self, compared_dirinfo):
        pass

    def _get_dirinfo(self):
        dirinfo = {}
        for target in self._get_sensor_config('directories'):
            self._do_get_dirinfo(target, dirinfo)

        return dirinfo

    def _do_get_dirinfo(self, target, results):
        if os.path.exists(target):
            if os.path.isdir(target):
                for fname in os.listdir(target):
                    self._do_get_dirinfo("%s/%s" % (target, fname), results)
            else:
                results[target] = os.stat(target).st_mtime

    def _get_sensor_config(self, key):
        sensor_conf = self.config.get('sensor', None)

        if sensor_conf:
            return sensor_conf.get(key, None)

    def _dispatch_trigger(self, path, time, status):
        payload = {
            'path': path,
            'time': time,
            'status': status,
        }
        self._sensor_service.dispatch(trigger="mypack.changed_file", payload=payload)

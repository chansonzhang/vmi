class Process(object):
    def __init__(self, name, pid, uid, gid, start_time, dtb=None, offset=None):
        self.offset = offset
        self.name = name
        self.pid = pid
        self.uid = uid
        self.gid = gid
        self.start_time = start_time
        self.dtb = dtb
        self.offset = offset

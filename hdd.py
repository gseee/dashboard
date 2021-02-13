import psutil

def get_hdd_data():
    name_hdd = []
    hdd_list = []
    for h in psutil.disk_partitions():
        name_hdd.append(h[0])

    for d in name_hdd:
        hdd_list.append([bytes2human(psutil.disk_usage(d).total), bytes2human(psutil.disk_usage(d).used), bytes2human(psutil.disk_usage(d).free),
                         psutil.disk_usage(d).percent])

    return name_hdd, hdd_list

def bytes2human(n):
    # http://code.activestate.com/recipes/578019
    # >>> bytes2human(10000)
    # '9.8K'
    # >>> bytes2human(100001221)
    # '95.4M'
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n
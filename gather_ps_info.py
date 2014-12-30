#!/usr/bin/env python
import psutil


MINIMUM_PERCENT = 5


def gen_ps_info():
    ps = []
    for proc in psutil.process_iter():
        try:
            cpu_percent = proc.get_cpu_percent(interval=0.001)
            if cpu_percent:
                memory_percent = proc.memory_percent()
                connections = len(proc.get_connections())
                threads = proc.get_num_threads()

                ps.append({
                    'name': proc.name(),
                    'cpu_percent': cpu_percent,
                    'memory_percent': '{0:.2g}'.format(memory_percent),
                    'connections': connections,
                    'threads': threads,
                    'username': proc.username(),
                    'pid': proc.pid
                })
        except psutil.NoSuchProcess:
            pass
    return ps


def gen_order_ps(max_processes=7):
    ps = gen_ps_info()
    ordered_ps = sorted(ps, key=lambda k: k['cpu_percent'], reverse=True)
    ps = []
    for proc in ordered_ps:
        msg = "name: {}\nCPU: {}%\nMemory Used: {}%\nConnections: {}\nThreads: {}\npid: {}\nusername: {}\n"
        ps_info = msg.format(proc['name'],
                             proc['cpu_percent'],
                             proc['memory_percent'],
                             proc['connections'],
                             proc['threads'],
                             proc['pid'],
                             proc['username'])
        ps.append(ps_info)
        if (max_processes == len(ps)) and (proc['cpu_percent'] < MINIMUM_PERCENT):
            return ps
    return ps


def main():
    print("starting ...")
    for p in gen_order_ps():
        print p

main()

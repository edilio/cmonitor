#!/usr/bin/env python
import influxdb
import psutil
import platform
import os
import time

CLIENT_ID = int(os.environ.get('CLIENT_ID', '0'))
DEVICE_ID = os.environ.get('DEVICE_ID')
NODE = platform.node()
INTERVAL = int(os.environ.get('INTERVAL', '1'))

INFLUX_USERNAME = os.environ.get('INFLUX_USERNAME')
INFLUX_PASSWORD = os.environ.get('INFLUX_PASSWORD')
INFLUX_DB = os.environ.get('INFLUX_DB')
INFLUX_HOST = os.environ.get('INFLUX_HOST', 'localhost')
INFLUX_PORT = os.environ.get('INFLUX_PORT', '8086')

db = influxdb.InfluxDBClient(INFLUX_HOST, INFLUX_PORT, INFLUX_USERNAME, INFLUX_PASSWORD, INFLUX_DB)

fields = ['client_id', 'device_id', 'node',
          'cpu_times_user', "cpu_times_nice", "cpu_times_system", "cpu_times_idle", "cpu_percent",
          'mem_total', 'mem_available', 'mem_percent', 'mem_used', 'mem_free', 'mem_active', 'mem_inactive', 'mem_wired'
          ]

one_mb = 1024.0
one_gb = 1024 * one_mb


def get_mb(number):
    return number / one_mb


def get_gb(number):
    return number / one_gb


def get_points():
    cpu_times = psutil.cpu_times()
    cpu_percent = psutil.cpu_percent(interval=None)
    memory = psutil.virtual_memory()
    point = [CLIENT_ID, DEVICE_ID, NODE,
             cpu_times.user, cpu_times.nice, cpu_times.system, cpu_times.idle, cpu_percent, get_gb(memory.total),
             get_gb(memory.available), memory.percent, get_gb(memory.used), get_gb(memory.free),
             get_gb(memory.active), get_gb(memory.inactive), get_gb(memory.wired)]
    return [point]


def insert_to_influx():
    points = get_points()

    data = [{"points": points,
             "name": "Monitoring",
             "columns": fields}]
    db.write_points(data=data, batch_size=1000)
    print("inserted")


print(INTERVAL)

while True:
    insert_to_influx()
    time.sleep(INTERVAL)

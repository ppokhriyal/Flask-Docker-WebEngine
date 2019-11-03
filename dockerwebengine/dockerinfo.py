import docker
from flask import Flask, jsonify
from cpuinfo import get_cpu_info
from psutil import virtual_memory


def info():

	cpu_info = get_cpu_info()
	return jsonify(cpu=cpu_info)


info()	
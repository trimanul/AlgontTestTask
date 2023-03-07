from monitors.cpu_monitor import CPUMonitor
import threading
import logging
import json

if __name__ == "__main__":
    cpu_monitor = CPUMonitor()

    cpu_monitor.run()

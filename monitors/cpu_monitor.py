import json
import sqlalchemy as sa
from utils.utils import load_config
from monitors.models import CPULoad
from sqlalchemy.orm import Session
from psutil import cpu_percent
import datetime
import threading
from time import sleep
import threading
import logging

class BaseMonitor():
    """
    Base monitor class
    """
    def __init__(self) -> None:
        self.db_config = load_config()["db_config"]
        db_url = sa.URL.create(
            f'{self.db_config["db_engine"]}+{self.db_config["db_dialect"]}',
            database=self.db_config["db_path"])
        
        self.engine = sa.create_engine(db_url)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
        self.logger.addHandler(handler)

        
class CPUMonitor(BaseMonitor):
    """
    CPU monitor class
    """

    def record_load(self) -> None:
        """
        Gets current CPU load and saves it into database
        """

        current_cpu_load = cpu_percent()
        
        record = CPULoad(monitor_datetime=datetime.datetime.now(), cpu_value=current_cpu_load)
        self.logger.debug(f"Recorded {record}")
        with Session(self.engine) as session:
            session.add(record)
            session.commit()


    def start_recording(self) -> None:
        while True:
            self.record_load()
            sleep(5)

    def run(self) -> None:
        """
        Starts cpu monitor thread
        """
        self.logger.debug(f"Monitor started")
        monitor_thread = threading.Thread(target=self.start_recording, daemon=True)
        monitor_thread.start()


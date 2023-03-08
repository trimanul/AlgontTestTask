import sqlalchemy as sa
import json
from utils.utils import load_config
from setuptools import setup

setup(
        name="algont_test_kudinov",
        version="0.5.0",
        install_requires=[
                'Flask == 2.2.3',
                'SQLAlchemy == 2.0.2',
                'psutil == 5.6.7',
                'importlib-metadata; python_version == "3.11"',
        ],
)


config = load_config()["db_config"]

db_url = sa.URL.create(
            f'{config["db_engine"]}+{config["db_dialect"]}',
            database=config["db_path"])

engine = sa.create_engine(db_url)

meta = sa.MetaData()

cpu_load_table = sa.Table(
        "cpu_load",
        meta,
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("monitor_datetime", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("cpu_value", sa.Float)
)

meta.create_all(engine)


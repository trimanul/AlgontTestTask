import sqlalchemy as sa
import json

with open("./config.json") as config_file:
            config = json.load(config_file)

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


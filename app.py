from monitors.models import CPULoad
from flask import Flask, render_template
from flask.json import jsonify
from sqlalchemy.orm import Session
import sqlalchemy as sa
from utils.utils import load_config
from monitors.cpu_monitor import CPUMonitor
import datetime
from utils.utils import detect_gaps

app = Flask(__name__, static_url_path='/static')

db_config = load_config()["db_config"]
engine = sa.create_engine(sa.URL.create(
        f'{db_config["db_engine"]}+{db_config["db_dialect"]}',
        database=db_config["db_path"]
))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cpu_load")
def cpu_load():
    hour_ago = datetime.datetime.now()
    hour_ago -= datetime.timedelta(hours=1)
    
    points: list[dict] = []

    stmt = sa.select(CPULoad).filter(CPULoad.monitor_datetime >= hour_ago)
    with Session(engine) as session:
        for row in session.scalars(stmt):
            points.append({"x": row.monitor_datetime, "y": row.cpu_value})
    
    # Реализация разрывов в графике
    points = detect_gaps(points, hour_ago, 720, 5)
    for point in points:
        point["x"] = point["x"].isoformat()
        
    
    return jsonify(points)

@app.route("/cpu_load_latest")
def cpu_load_latest():
    hour_ago = datetime.datetime.now()
    hour_ago -= datetime.timedelta(hours=1)

    stmt = sa.select(CPULoad).filter(CPULoad.monitor_datetime >= hour_ago).order_by(CPULoad.monitor_datetime.desc())
    with Session(engine) as session:
        row = session.scalars(stmt).first()
        point = {"x": row.monitor_datetime.isoformat(), "y": row.cpu_value}
    
    return jsonify(point)

@app.route("/cpu_load_avg")       
def cpu_load_avg():
    hour_ago = datetime.datetime.now()
    hour_ago -= datetime.timedelta(hours=1)
    
    points: list[dict] = []

    stmt = sa.text(f"SELECT cpu_load.monitor_datetime, CAST(strftime('%M', cpu_load.monitor_datetime)AS INTEGER) as minute, avg(cpu_load.cpu_value) as average\
                   FROM cpu_load WHERE CAST(strftime('%H', cpu_load.monitor_datetime) AS INTEGER) >= {hour_ago.hour} AND minute >= {hour_ago.minute} AND strftime('%d', cpu_load.monitor_datetime) LIKE '%{hour_ago.day}%' GROUP BY minute;")
    with Session(engine) as session:
        for row in session.execute(stmt):
            monitor_datetime, _, cpu_value = row
            points.append({"x": datetime.datetime.fromisoformat(monitor_datetime), "y": cpu_value})
    
    # Реализация разрывов в графике
    points = detect_gaps(points, hour_ago, 60, 60)
    for point in points:
        point["x"] = point["x"].isoformat()
        
    
    return jsonify(points)

@app.route("/cpu_load_avg_latest")
def cpu_load_avg_latest():
    hour_ago = datetime.datetime.now()
    hour_ago -= datetime.timedelta(hours=1)

    stmt = sa.text(f"SELECT cpu_load.monitor_datetime, strftime('%M', cpu_load.monitor_datetime) as minute, avg(cpu_load.cpu_value) as average\
                   FROM cpu_load WHERE CAST(strftime('%H', cpu_load.monitor_datetime) AS INTEGER) >= {hour_ago.hour} AND strftime('%d', cpu_load.monitor_datetime) LIKE '%{hour_ago.day}%' GROUP BY minute ORDER BY cpu_load.monitor_datetime DESC;")
    with Session(engine) as session:
        row = session.execute(stmt).first()
        monitor_datetime, _, cpu_value = row
        point = {"x": monitor_datetime, "y": cpu_value}
    
    return jsonify(point)

if __name__ == "__main__":
    cpu_monitor = CPUMonitor()
    cpu_monitor.run()
    app.run()




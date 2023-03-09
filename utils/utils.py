import json
import datetime

def load_config() -> dict:
        """
        Loads config file from json file ("config.json")
        """
        with open("./config.json") as config_file:
            json_config = json.load(config_file)

        return json_config

def detect_gaps(points: list[dict], begin_datetime: datetime.datetime,desired_length: int, seconds_gap:int) -> list[dict]:
    """
    Tear detection function
    Takes array of graph points,
    beginning datetime of detection window,
    desired length of array, 
    minimal gap between points in seconds.
    Returns array, padded with gaps
    """
    if len(points) == 0:
        return []

    point_array = points[:]

    if len(point_array) < desired_length:
        for ind, point in enumerate(point_array):
            if (ind == (len(point_array) - 1)):
                break
            cur_time = point["x"]
            next_time = point_array[(ind + 1)]["x"]
            delta = abs(cur_time - next_time)
            if (delta).seconds > seconds_gap:
                point_array.insert(ind + 1, {"x": point["x"] + datetime.timedelta(seconds=seconds_gap), "y": None})

    if ((point_array[0]["x"] - begin_datetime).seconds > seconds_gap):
        step = begin_datetime
        while ((begin_datetime - step).seconds > seconds_gap):
            point_array.insert(0, {"x":step, "y": None})
            step += datetime.timedelta(seconds=seconds_gap)

    return point_array
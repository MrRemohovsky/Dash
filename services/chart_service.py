import numpy as np
import plotly.express as px
import pandas as pd
from datetime import datetime


class ChartTypeSelector:
    def __init__(self, title):
        # self.sensor_type = sensor_type
        # self.dict_chart_types = {
        #     "thermocouple": px.line,
        #     "ammeter": px.box,
        #     "accelerometer": px.line,
        #     "tachometer": px.line,
        #     "speed_sensor": px.line,
        #     "anemometer": px.line,
        # }
    # def get_chart_type(self):
    #     return self.dict_chart_types.get(self.sensor_type, px.line)
        self.title = title
        self.dict_chart_types = {
            "mixer_engine_temperature": px.line,
            "mixer_current_consumption": px.scatter,
            "mixer_vibration": px.box,
            "mixer_rotation_speed": px.violin,
            "belt_movement_speed": px.line,
            "conveyor_current_consumption": px.histogram,
            "conveyor_vibration": px.strip,
            "conveyor_motor_temperature": px.ecdf,
            "furnace_temperature": px.density_contour,
            "furnace_current_consumption": px.density_heatmap,
            "cooling_temperature": px.scatter,
            "airflow_speed": px.histogram
        }

    def get_chart_type(self):
        return self.dict_chart_types.get(self.title, px.line)


class ChartService:
    @staticmethod
    def build_chart(time_series, title, sensor_type, unit):
        df = pd.DataFrame(time_series)
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        graph = ChartTypeSelector(title).get_chart_type()

        if graph in [px.density_heatmap, px.density_contour]:
            fig = graph(
                df,
                x="timestamp",
                y="value",
                title=title,
                labels={"timestamp": "Time", "value": f"value {unit}"}
            )
        elif graph == px.ecdf:
            fig = graph(
                df,
                x="value",
                title=title,
                labels={"value": f"value {unit}"}
            )
        else:
            fig = graph(
                df,
                x="timestamp",
                y="value",
                title=title,
                labels={"timestamp": "Time", "value": f"value {unit}"}
            )

        return fig

    @staticmethod
    def filter_chart(time_series, start_date, end_date):
        start = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
        end = datetime.fromisoformat(end_date.replace("Z", "+00:00"))

        filtered = [
            record for record in time_series
            if start <= datetime.fromisoformat(record["timestamp"].replace("Z", "+00:00")) <= end
        ]
        return filtered
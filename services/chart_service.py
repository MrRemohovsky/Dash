import numpy as np
import plotly.express as px
import pandas as pd
from datetime import datetime


class ChartTypeSelector:
    def __init__(self, title):
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

        #graph = ChartTypeSelector(title).get_chart_type()
        fig = px.line(df, x='timestamp', y='value', title=title, labels={"timestamp": "Time", "value": f"value {unit}"})
        # if graph in [px.density_heatmap, px.density_contour]:
        #     fig = graph(
        #         df,
        #         x="timestamp",
        #         y="value",
        #         title=title,
        #         labels={"timestamp": "Time", "value": f"value {unit}"}
        #     )
        # elif graph == px.ecdf:
        #     fig = graph(
        #         df,
        #         x="value",
        #         title=title,
        #         labels={"value": f"value {unit}"}
        #     )
        # else:
        #     fig = graph(
        #         df,
        #         x="timestamp",
        #         y="value",
        #         title=title,
        #         labels={"timestamp": "Time", "value": f"value {unit}"}
        #     )

        return fig

    @staticmethod
    def filter_chart(time_series, start_date, end_date):
        start = pd.to_datetime(start_date.replace("Z", "+00:00"))
        end = pd.to_datetime(end_date.replace("Z", "+00:00"))

        df = pd.DataFrame(time_series)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        filtered_df = df[(df['timestamp'] >= start) & (df['timestamp'] <= end)]

        return filtered_df.to_dict('records')
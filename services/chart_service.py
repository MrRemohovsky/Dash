import plotly.express as px
import pandas as pd

class ChartTypeSelector:
    def __init__(self, title, df, unit):
        self.title = title
        self.df = df
        self.unit = unit
        self.dict_chart_types = {
            "mixer_engine_temperature":
                px.density_heatmap(
                df,
                x="timestamp",
                y="value",
                title=title,
                labels={"timestamp": "Time", "value": f"{unit}"},
                color_continuous_scale="Viridis",
                ),
            "mixer_current_consumption":
                px.scatter(
                    df,
                    x="timestamp",
                    y="value",
                    title=title,
                    labels={"timestamp": "Time", "value": f"{unit}"},
                    color='value',
                ),
            "mixer_vibration":
                px.histogram(
                    df,
                    x="timestamp",
                    y="value",
                    title=title,
                    labels={"timestamp": "Time", "value": f"{unit}"},
                    color_discrete_sequence=['purple'],
                ).update_layout(bargap=0.1),
            "conveyor_vibration":
                px.histogram(
                    df,
                    x="timestamp",
                    y="value",
                    title=title,
                    labels={"timestamp": "Time", "value": f"{unit}"},
                    color_discrete_sequence=['green'],
                ).update_layout(bargap=0.1),
            "conveyor_motor_temperature":
                px.density_heatmap(
                df,
                x="timestamp",
                y="value",
                title=title,
                labels={"timestamp": "Time", "value": f"{unit}"},
                color_continuous_scale="Spectral",
                ),
            "furnace_temperature":
                px.scatter(
                    df.iloc[::10],
                    x="timestamp",
                    y="value",
                    title=title,
                    labels={"timestamp": "Time", "value": f"{unit}"},
                    color_continuous_scale="Viridis",
                ).update_traces(marker=dict(size=10))
        }

    def get_chart_info(self):
        return self.dict_chart_types.get(
            self.title,
            px.line(
                self.df,
                x="timestamp",
                y="value",
                title=self.title,
                labels={"timestamp": "Time", "value": f"{self.unit}"},
                color_discrete_sequence=['black']
            ),
        )

class ChartService:
    @staticmethod
    def build_chart(time_series, title, sensor_type, unit):
        df = pd.DataFrame(time_series)
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        fig = ChartTypeSelector(title, df, unit).get_chart_info()

        fig.update_layout(
            margin=dict(l=10, r=10, t=50, b=10),
            plot_bgcolor='rgba(245, 245, 220, 1)',
            paper_bgcolor='rgba(47, 79, 79, 1)',
            font_color='white'
        )

        return fig
import plotly.express as px
import pandas as pd
from datetime import datetime


class ChartService:

    @staticmethod
    def build_chart(time_series, title):
        df = pd.DataFrame(time_series)
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        fig = px.line(
            df,
            x="timestamp",
            y="value",
            title=title,
            labels={"timestamp": "Time", "value": "Value"}
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
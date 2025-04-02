from dash import html, dcc, Output, Input
from services.chart_service import ChartService
from models import Factory, Device, Chart

class DashboardApp:
    def __init__(self, dash_app):
        self.dash_app = dash_app
        self._setup_layout()
        self._register_callbacks()

    def _setup_layout(self):
        with self.dash_app.server.app_context():
            factories = Factory.query.all()

        self.dash_app.layout = html.Div([
            html.Div([
                html.Div([
                    html.Label("Завод:", className="form-label selector-label"),
                    dcc.Dropdown(
                        id='factory-selector',
                        options=[{'label': factory.title, 'value': factory.id} for factory in factories],
                        value=None,
                        placeholder="Выберите завод",
                        className="selector"
                    ),
                ], className="selector-wrapper"),
                html.Div([
                    html.Label("Устройство:", className="form-label selector-label"),
                    dcc.Dropdown(
                        id='device-selector',
                        options=[],
                        value=None,
                        placeholder="Выберите устройство",
                        className="selector"
                    ),
                ], className="selector-wrapper"),
                html.Div([
                    html.Label("Диапазон дат:", className="form-label selector-label date-label"),
                    dcc.DatePickerRange(
                        id='date-picker-range',
                        start_date="2025-03-20",
                        end_date="2025-03-22",
                        display_format='YYYY-MM-DD',
                        className="selector date-picker"
                    ),
                ], className="selector-wrapper"),
            ], className="selector-container"),
            html.Div(id='charts-container', className="row charts-container")
        ], className="container-fluid dash-background")

    def _get_device_options(self, factory_id):
        if not factory_id:
            return []
        with self.dash_app.server.app_context():
            devices = Device.query.filter_by(factory_id=factory_id).all()
            return [{'label': device.title, 'value': device.id} for device in devices]

    def _get_chart_elements(self, factory_id, device_id, start_date, end_date):
        chart_elements = []
        with self.dash_app.server.app_context():
            filtered_charts = Chart.query.join(Device).filter(
                Chart.device_id == device_id,
                Device.factory_id == factory_id
            ).all() if factory_id and device_id else []

            for chart in filtered_charts:
                filtered_time_series = ChartService.filter_chart(chart.time_series, start_date, end_date)
                if filtered_time_series:
                    fig = ChartService.build_chart(filtered_time_series, chart.title)
                    chart_elements.append(
                        html.Div(
                            dcc.Graph(figure=fig, style={'height': '300px'}),
                            className="col-md-6 mb-2"
                        )
                    )
        return chart_elements if chart_elements else None

    def _register_callbacks(self):
        @self.dash_app.callback(
            Output('device-selector', 'options'),
            Input('factory-selector', 'value')
        )
        def update_device_selector(factory_id):
            return self._get_device_options(factory_id)

        @self.dash_app.callback(
            Output('charts-container', 'children'),
            Input('factory-selector', 'value'),
            Input('device-selector', 'value'),
            Input('date-picker-range', 'start_date'),
            Input('date-picker-range', 'end_date')
        )
        def update_charts(factory_id, device_id, start_date, end_date):
            return self._get_chart_elements(factory_id, device_id, start_date, end_date)

def init_dashboard(dash_app):
    return DashboardApp(dash_app)
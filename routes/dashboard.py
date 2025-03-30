import os
from dash import html, dcc, callback, Output, Input
from services.chart_service import ChartService
from models import Factory, Device, Chart

def init_dashboard(dash_app):
    navbar_path = os.path.join(dash_app.server.static_folder, 'navbar.html')
    with open(navbar_path, 'r', encoding='utf-8') as f:
        navbar_content = f.read()
    with dash_app.server.app_context():
        charts = Chart.query.all()
        factories = Factory.query.all()
        devices = Device.query.all()

    dash_app.layout = html.Div([
        dcc.Markdown(navbar_content, dangerously_allow_html=True),
        html.H1("Dashboard with Charts"),
        # Селектор завода
        html.Label("Select Factory:"),
        dcc.Dropdown(
            id='factory-selector',
            options=[{'label': factory.title, 'value': factory.id} for factory in factories],
            value=None,
            placeholder="Select a factory"
        ),
        # Селектор устройства
        html.Label("Select Device:"),
        dcc.Dropdown(
            id='device-selector',
            options=[],
            value=None,
            placeholder="Select a device"
        ),
        # Фильтр по дате
        dcc.DatePickerRange(
            id='date-picker-range',
            start_date="2025-03-20",
            end_date="2025-03-22",
            display_format='YYYY-MM-DD'
        ),
        html.Div(id='charts-container')
    ])

    # Callback для обновления списка устройств
    @callback(
        Output('device-selector', 'options'),
        Input('factory-selector', 'value')
    )
    def update_device_selector(factory_id):
        if not factory_id:
            return []
        with dash_app.server.app_context():
            devices = Device.query.filter_by(factory_id=factory_id).all()
            return [{'label': device.title, 'value': device.id} for device in devices]

    @callback(
        Output('charts-container', 'children'),
        Input('factory-selector', 'value'),
        Input('device-selector', 'value'),
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date')
    )
    def update_charts(factory_id, device_id, start_date, end_date):
        chart_elements = []
        with dash_app.server.app_context():
            filtered_charts = Chart.query.join(Device).filter(Chart.device_id==device_id).filter(Device.factory_id==factory_id).all() \
            if factory_id and device_id else []

            for chart in filtered_charts:
                filtered_time_series = ChartService.filter_chart(chart.time_series, start_date, end_date)
                if filtered_time_series:
                    fig = ChartService.build_chart(filtered_time_series, chart.title)
                    chart_elements.append(dcc.Graph(figure=fig))
        return chart_elements if chart_elements else [html.P("No data for the selected filters.")]
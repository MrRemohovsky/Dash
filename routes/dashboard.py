from dash import html, dcc, Output, Input
from core.utils import login_required
from services.chart_service import ChartService
from models import Factory, Equipment, Chart
from flask import render_template, Blueprint

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/charts')
@login_required
def dash_page():
    return render_template('dash_page.html')

@dashboard.route('/dashboard/')
@login_required
def render_dash():
    from app import dash_app
    return dash_app.index()

class DashboardApp:
    def __init__(self, dash_app):
        self.dash_app = dash_app
        with self.dash_app.server.app_context():
            self.factories = Factory.query.all()
        self._setup_layout()
        self._register_callbacks()

    def _setup_layout(self):
        self.dash_app.layout = html.Div([
            html.Div([
                html.Div([
                    html.Label("Завод:", className="form-label selector-label"),
                    dcc.Dropdown(
                        id='factory-selector',
                        options=[{'label': factory.title, 'value': factory.id} for factory in self.factories],
                        value=self.factories[0].id if self.factories else None,
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
                        display_format='DD-MM-YYYY',
                        className="selector date-picker"
                    ),
                ], className="selector-wrapper"),
            ], className="selector-container"),
            html.Div(id='charts-container', className="row charts-container")
        ], className="container-fluid dash-background")

    def _get_chart_elements(self, factory_id, equipment_id, start_date, end_date):
        if not factory_id or not equipment_id or not start_date or not end_date:
            return [html.P("Нет данных за выбранный промежуток времени")]
        chart_elements = []
        with self.dash_app.server.app_context():
            charts = Chart.query.join(Equipment).filter(
                Chart.equipment_id == equipment_id,
                Equipment.factory_id == factory_id
            ).all() if factory_id and equipment_id else []

            for chart in charts:
                filtered_time_series = ChartService.filter_chart(chart.time_series, start_date, end_date)
                if filtered_time_series:
                    fig = ChartService.build_chart(filtered_time_series, chart.title, chart.sensor_type, chart.unit)
                    chart_elements.append(
                        html.Div(
                            dcc.Graph(figure=fig, style={'height': '300px'}),
                            className="col-md-6 mb-2"
                        )
                    )
        return chart_elements if chart_elements else None

    def _register_callbacks(self):
        @self.dash_app.callback(
            [Output('device-selector', 'options'),  # Выводим опции
             Output('device-selector', 'value')],  # Выводим значение для выбора первого
            Input('factory-selector', 'value')
        )
        def update_equipment_selector(factory_id):
            if not factory_id:
                return [], None
            with self.dash_app.server.app_context():
                equipments = Equipment.query.filter_by(factory_id=factory_id).all()
                options = [{'label': f'{equipment.title}-{equipment.position[-2:]}', 'value': equipment.id} for equipment in equipments]
                return options, options[0]['value'] if options else None

        @self.dash_app.callback(
            Output('charts-container', 'children'),
            Input('factory-selector', 'value'),
            Input('device-selector', 'value'),
            Input('date-picker-range', 'start_date'),
            Input('date-picker-range', 'end_date')
        )
        def update_charts(factory_id, equipment_id, start_date, end_date):
            return self._get_chart_elements(factory_id, equipment_id, start_date, end_date)

def init_dashboard(dash_app):
    return DashboardApp(dash_app)
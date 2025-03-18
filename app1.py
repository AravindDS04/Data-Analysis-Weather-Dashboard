import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import requests
import time

# OpenWeatherMap API key
API_KEY = "8ae04ecd91cc24827d865389a525856a"

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Weather Data Analysis Dashboard"

# Layout of the dashboard
app.layout = html.Div(
    style={"backgroundColor": "#f4f4f4", "padding": "20px"},
    children=[
        html.H1(
            "Weather Data Analysis Dashboard",
            style={"textAlign": "center", "color": "#2c3e50", "marginBottom": "20px"},
        ),
        html.Div(
            style={"display": "flex", "justifyContent": "center", "marginBottom": "20px"},
            children=[
                dcc.Dropdown(
                    id="city-dropdown",
                    options=[
                        {"label": "New York", "value": "New York"},
                        {"label": "London", "value": "London"},
                        {"label": "Tokyo", "value": "Tokyo"},
                        {"label": "Sydney", "value": "Sydney"},
                        {"label": "Paris", "value": "Paris"},
                        {"label": "India", "value": "India"},
                    ],
                    value="New York",
                    clearable=False,
                    style={"width": "300px"},
                ),
            ],
        ),
        html.Div(
            style={"display": "flex", "justifyContent": "space-around", "marginBottom": "20px"},
            children=[
                html.Div(
                    id="temperature-metric",
                    style={
                        "backgroundColor": "#3498db",
                        "color": "white",
                        "padding": "20px",
                        "borderRadius": "10px",
                        "textAlign": "center",
                        "width": "30%",
                    },
                ),
                html.Div(
                    id="humidity-metric",
                    style={
                        "backgroundColor": "#2ecc71",
                        "color": "white",
                        "padding": "20px",
                        "borderRadius": "10px",
                        "textAlign": "center",
                        "width": "30%",
                    },
                ),
                html.Div(
                    id="wind-speed-metric",
                    style={
                        "backgroundColor": "#e74c3c",
                        "color": "white",
                        "padding": "20px",
                        "borderRadius": "10px",
                        "textAlign": "center",
                        "width": "30%",
                    },
                ),
            ],
        ),
        html.Div(
            style={"display": "flex", "justifyContent": "space-around", "marginBottom": "20px"},
            children=[
                dcc.Graph(id="temperature-chart", style={"width": "48%"}),
                dcc.Graph(id="humidity-wind-chart", style={"width": "48%"}),
            ],
        ),
        dcc.Interval(id="interval-component", interval=60000, n_intervals=0),  # Update every 60 seconds
    ],
)

# Function to fetch weather data
def fetch_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
        }
    else:
        return None

# Callback to update the dashboard
@app.callback(
    [
        Output("temperature-metric", "children"),
        Output("humidity-metric", "children"),
        Output("wind-speed-metric", "children"),
        Output("temperature-chart", "figure"),
        Output("humidity-wind-chart", "figure"),
    ],
    [Input("city-dropdown", "value"), Input("interval-component", "n_intervals")],
)
def update_dashboard(city, n):
    # Fetch weather data
    weather_data = fetch_weather_data(city)
    if not weather_data:
        return ["N/A", "N/A", "N/A", {}, {}]

    # Update metrics
    temperature = f"Temperature: {weather_data['temperature']} °C"
    humidity = f"Humidity: {weather_data['humidity']} %"
    wind_speed = f"Wind Speed: {weather_data['wind_speed']} m/s"

    # Simulate historical data for charts
    historical_data = pd.DataFrame({
        "Time": pd.date_range(start="2023-01-01", periods=10, freq="H"),
        "Temperature": [weather_data["temperature"] + i for i in range(10)],
        "Humidity": [weather_data["humidity"] + i for i in range(10)],
        "Wind Speed": [weather_data["wind_speed"] + i for i in range(10)],
    })

    # Create charts
    temperature_chart = px.line(
        historical_data,
        x="Time",
        y="Temperature",
        title="Temperature Over Time",
        labels={"Temperature": "Temperature (°C)"},
        color_discrete_sequence=["#3498db"],
    )
    humidity_wind_chart = px.bar(
        historical_data,
        x="Time",
        y=["Humidity", "Wind Speed"],
        title="Humidity and Wind Speed Over Time",
        labels={"value": "Value", "variable": "Metric"},
        color_discrete_sequence=["#2ecc71", "#e74c3c"],
        barmode="group",
    )

    return [temperature, humidity, wind_speed, temperature_chart, humidity_wind_chart]

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
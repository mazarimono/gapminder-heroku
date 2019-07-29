# ❶ osのインポート
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output

gapminder = px.data.gapminder()

app = dash.Dash(__name__)

# ❷ 付け加える
server=app.server

# アプリケーションの外見の作成
app.layout = html.Div(
    [
        # 1段目　タイトル表示
        html.Div(
            [html.H1("Gapminder-Graph", style={"textAlign": "center"})],
            style={
                "width": "50%",
                "margin": "3% auto 3%",
                "backgroundColor": "#519D9E",
                "borderRadius": 15,
            },
        ),
        # 二段目　グラフ表示
        html.Div(
            [
                dcc.Graph(
                    id="gapminder-graph",
                    figure=px.scatter(
                        gapminder,
                        x="gdpPercap",
                        y="lifeExp",
                        size="pop",
                        color="continent",
                        animation_frame="year",
                        hover_name="country",
                        log_x=True,
                        range_y=[20, gapminder["lifeExp"].max() + 10],
                        size_max=60,
                        height=600,
                    ),
                )
            ],
            style={"width": "80%", "margin": "3% auto 3%", "height": 600},
        ),
        # 三段目　サブタイトル表示
        html.Div(
            [html.H2(id="bottom-title", style={"textAlign": "center"})],
            style={
                "width": "40%",
                "margin": "3% auto 3%",
                "backgroundColor": "#58C9B9",
                "borderRadius": 15,
            },
        ),
        #  四段目　3つのグラフ表示
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="left-graph")],
                    style={"width": "33.3%", "height": 300, "display": "inline-block"},
                ),
                html.Div(
                    [dcc.Graph(id="mid-graph")],
                    style={"width": "33.3%", "height": 300, "display": "inline-block"},
                ),
                html.Div(
                    [dcc.Graph(id="right-graph")],
                    style={"width": "33.3%", "height": 300, "display": "inline-block"},
                ),
            ],
            style={"width": "90%", "margin": "3% auto 3%"},
        ),
    ],
    style={"height": 1700, "backgroundColor": "#8afeb9", "padding": "3% 3%", "borderRadius": 15},
)

# hoverDataを利用してのコールバック
@app.callback(
    [   
        Output("bottom-title", "children"),
        Output("left-graph", "figure"),
        Output("mid-graph", "figure"),
        Output("right-graph", "figure"),
    ],
    [Input("gapminder-graph", "hoverData")],
)
def update_title(hoverData):
    if hoverData is None:
        country_name = "Japan"
    else:
        country_name = hoverData["points"][0]["hovertext"]

    country_df = gapminder[gapminder["country"] == country_name]

    return (
        country_name,
        px.line(
            country_df,
            x="year",
            y="gdpPercap",
            title="{}の一人当たりGDP".format(country_name),
        ),
        px.line(
            country_df, x="year", y="lifeExp", title="{}の平均余命".format(country_name)
        ),
        px.line(country_df, x="year", y="pop", title="{}の人口".format(country_name)),
    )

if __name__ == "__main__":
    app.run_server(debug=True)

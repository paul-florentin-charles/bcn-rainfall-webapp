from typing import Any

import plotly.graph_objs as go
import plotly.io
from plotly.subplots import make_subplots

DEFAULT_LAYOUT: dict[str, Any] = dict(
    legend={
        "yanchor": "top",
        "y": 0.99,
        "xanchor": "left",
        "x": 0.01,
        "bgcolor": "rgba(125, 125, 125, 0.7)",
    },
    font={
        "color": "white",
        "family": "Khula, sans-serif",
        "size": 11,
    },
    paper_bgcolor="rgba(34, 34, 34, 0.6)",
    plot_bgcolor="rgba(123, 104, 75, 0.3)",
    margin={"t": 65, "r": 30, "b": 45, "l": 55},
    xaxis={"title": {"standoff": 0}},
    yaxis={"title": {"standoff": 0}},
    title={"pad": {"t": 0, "r": 0, "b": 0, "l": 1000}},
    autosize=True,
)


def aggregate_plotly_json_figures(
    traces_json: list[str], *, layout: dict[str, Any] | None = None
) -> str:
    figure = go.Figure()
    for trace_json in traces_json:
        figure.add_traces(list(plotly.io.from_json(trace_json).select_traces()))

    figure.update_layout(
        {**DEFAULT_LAYOUT, **(layout or {})},
    )

    return figure.to_json()


def aggregate_plotly_json_pie_charts(
    traces_json: list[str],
    *,
    rows: int,
    cols: int,
    layout: dict[str, Any] | None = None,
    graph_labels: list[str] | None = None,
) -> str:
    figure = make_subplots(
        rows=rows,
        cols=cols,
        specs=[[{"type": "domain"} for _ in range(rows)] for _ in range(cols)],
    )

    for row in range(1, rows + 1):
        for col in range(1, cols + 1):
            figure.add_trace(
                list(
                    plotly.io.from_json(
                        traces_json[row - 1 + (col - 1) * rows]
                    ).select_traces()
                )[0],
                row=row,
                col=col,
            )

    figure.update_traces(hole=0.3, scalegroup="one")

    annotations: list[dict] = []
    if graph_labels:
        for row in range(1, rows + 1):
            for col in range(1, cols + 1):
                annotations.append(
                    {
                        "text": graph_labels[row - 1 + (col - 1) * rows],
                        "x": sum(figure.get_subplot(row, col).x) / 2,
                        "y": sum(figure.get_subplot(row, col).y) / 2,
                        "showarrow": False,
                        "xanchor": "center",
                        "yanchor": "middle",
                    }
                )

    figure.update_layout(
        {
            **DEFAULT_LAYOUT,
            "legend": {
                "yanchor": "middle",
                "y": 0.5,
                "xanchor": "center",
                "x": 0.5,
            },
            "annotations": annotations,
            **(layout or {}),
        },
    )

    return figure.to_json()

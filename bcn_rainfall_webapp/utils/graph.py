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
        "color": "#dfd0c1",
        "family": "Khula, sans-serif",
        "size": 11,
    },
    paper_bgcolor="rgba(34, 34, 34, 0.6)",
    plot_bgcolor="rgba(123, 104, 75, 0.3)",
    margin={"t": 65, "r": 30, "b": 45, "l": 65},
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
            traces = list(
                plotly.io.from_json(
                    traces_json[row - 1 + (col - 1) * rows]
                ).select_traces()
            )
            figure.add_trace(
                traces[0],  # We assume every Figure has only one trace in it
                row=row,
                col=col,
            )

    traces_options: dict[str, Any] = {"scalegroup": "one"}

    annotations: list[dict] = []
    if graph_labels:
        traces_options["hole"] = 0.3
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

    figure.update_traces(traces_options)

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

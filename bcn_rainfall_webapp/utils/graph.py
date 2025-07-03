from functools import reduce
from typing import Any

import pandas as pd
import plotly.express as px
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
    paper_bgcolor="rgba(34, 34, 34, 0.65)",
    plot_bgcolor="rgba(123, 104, 75, 0.25)",
    margin={"t": 65, "r": 30, "b": 45, "l": 65},
    autosize=True,
)


def sorted_vertical_bars_by_y_values(figure: go.Figure, descending=True) -> go.Figure:
    # 1. Extract vertical bar traces
    data_frames: list[pd.DataFrame] = []
    trace_names: list[str] = []
    for trace in figure.data:
        if isinstance(trace, go.Bar) and trace.orientation in {None, "v"}:
            data_frames.append(pd.DataFrame({"x": trace.x, trace.name: trace.y}))
            trace_names.append(trace.name)

    # 2. Merge all traces into one DataFrame
    if not data_frames:
        raise ValueError("No vertical bar traces found in figure.")

    df_all = reduce(lambda df1, df2: df1.merge(df2, on="x", how="outer"), data_frames)

    # 3. Get color list from layout or use default Plotly palette
    colorway: list[str] = px.colors.qualitative.Plotly
    if figure.layout.colorway:
        colorway = figure.layout.colorway

    # 4. Map trace names to colors
    color_map = {trace_names[idx]: colorway[idx] for idx in range(len(trace_names))}

    # 5. Sort segments per bar (row)
    sorted_segments: list[dict[str, Any]] = []
    for _, row in df_all.iterrows():
        sorted_row = row.drop("x").sort_values(ascending=not descending)
        for segment_name, y_val in sorted_row.items():
            sorted_segments.append(
                {
                    "x": row["x"],
                    "name": segment_name,
                    "y": y_val,
                    "color": color_map[segment_name],
                }
            )

    # 6. Create new micro-traces with correct colors
    sorted_traces: list[go.Bar] = []
    legend_shown: set[str] = set()
    for segment in sorted_segments:
        # Avoid duplicate legends and respect original legend order
        show_legend = False
        if segment["name"] not in legend_shown and segment["name"] == trace_names[-1]:
            show_legend = True
            legend_shown.add(segment["name"])
            del trace_names[-1]

        sorted_traces.append(
            go.Bar(
                x=[segment["x"]],
                y=[segment["y"]],
                name=segment["name"],
                marker={"color": segment["color"]},
                legendgroup=segment["name"],
                showlegend=show_legend,
            )
        )

    layout = figure.layout
    layout.update(
        legend={
            "tracegroupgap": 0
        },  # Somehow legends have a vertical gap between them if we don't set this to 0.
    )

    return go.Figure(data=sorted_traces, layout=layout)


def aggregate_plotly_json_figures(
    traces_json: list[str],
    *,
    layout: dict[str, Any] | None = None,
) -> go.Figure:
    figure = go.Figure()
    for trace_json in traces_json:
        figure.add_traces(list(plotly.io.from_json(trace_json).select_traces()))

    figure.update_layout(
        {**DEFAULT_LAYOUT, **(layout or {})},
    )

    return figure


def aggregate_plotly_json_pie_charts(
    traces_json: list[str],
    *,
    rows: int,
    cols: int,
    layout: dict[str, Any] | None = None,
    graph_labels: list[str] | None = None,
) -> go.Figure:
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

    return figure

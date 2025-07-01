import json

import plotly.graph_objects as go

from bcn_rainfall_webapp.utils.graph import (
    aggregate_plotly_json_figures,
    aggregate_plotly_json_pie_charts,
    sorted_vertical_bars_by_y_values,
)


class TestUtilsGraph:
    @staticmethod
    def test_aggregate_plotly_json_figures_simple():
        plotly_traces = [
            json.dumps({"data": [{"type": "scatter", "y": [1, 2, 3]}], "layout": {}})
        ]
        result = aggregate_plotly_json_figures(plotly_traces)

        assert isinstance(result, str)
        assert "scatter" in result

    @staticmethod
    def test_aggregate_plotly_json_figures_multiple():
        plotly_traces = [
            json.dumps({"data": [{"type": "bar", "y": [1, 2, 3]}], "layout": {}}),
            json.dumps({"data": [{"type": "scatter", "y": [3, 2, 1]}], "layout": {}}),
        ]
        result = aggregate_plotly_json_figures(plotly_traces)

        assert isinstance(result, str)
        assert "bar" in result and "scatter" in result

    @staticmethod
    def test_aggregate_plotly_json_figures_with_layout():
        plotly_traces = [
            json.dumps({"data": [{"type": "scatter", "y": [1, 2, 3]}], "layout": {}})
        ]
        result = aggregate_plotly_json_figures(
            plotly_traces, layout={"title": "Custom Title"}
        )

        assert isinstance(result, str)
        assert "Custom Title" in result

    @staticmethod
    def test_aggregate_plotly_json_pie_charts_basic():
        pie_jsons = [
            json.dumps(
                {
                    "data": [{"type": "pie", "labels": ["A", "B"], "values": [1, 2]}],
                    "layout": {},
                }
            )
            for _ in range(4)
        ]
        result = aggregate_plotly_json_pie_charts(pie_jsons, rows=2, cols=2)

        assert isinstance(result, str)
        assert result.count("pie") >= 4

    @staticmethod
    def test_aggregate_plotly_json_pie_charts_with_labels():
        pie_jsons = [
            json.dumps(
                {
                    "data": [{"type": "pie", "labels": ["A", "B"], "values": [1, 2]}],
                    "layout": {},
                }
            )
            for _ in range(4)
        ]
        labels = ["Spring", "Summer", "Fall", "Winter"]
        result = aggregate_plotly_json_pie_charts(
            pie_jsons, rows=2, cols=2, graph_labels=labels
        )

        for label in labels:
            assert label in result

    @staticmethod
    def test_sorted_vertical_bars_by_y_values_simple():
        figure = go.Figure()
        figure.add_bar(x=[1, 2, 3], y=[2, 3, 1], name="A")
        sorted_fig = sorted_vertical_bars_by_y_values(figure, descending=True)
        # Only one trace, so y values should remain in original order per x

        assert [bar.y[0] for bar in sorted_fig.data] == [2, 3, 1]

    @staticmethod
    def test_sorted_vertical_bars_by_y_values_ascending():
        figure = go.Figure()
        figure.add_bar(x=[1, 2, 3], y=[2, 3, 1], name="A")
        sorted_fig = sorted_vertical_bars_by_y_values(figure, descending=False)

        assert [bar.y[0] for bar in sorted_fig.data] == [2, 3, 1]

    @staticmethod
    def test_sorted_vertical_bars_by_y_values_multiple_traces():
        figure = go.Figure()
        figure.add_bar(x=[1, 2], y=[5, 2], name="A")
        figure.add_bar(x=[1, 2], y=[3, 4], name="B")

        # For each x, collect y values and check they are sorted descending
        x_to_ys: dict[int, list[int]] = {}
        for bar in sorted_vertical_bars_by_y_values(figure, descending=True).data:
            x = bar.x[0]
            y = bar.y[0]
            x_to_ys.setdefault(x, []).append(y)
        for ys in x_to_ys.values():
            assert ys == sorted(ys, reverse=True)

        # Also test ascending
        x_to_ys = {}
        for bar in sorted_vertical_bars_by_y_values(figure, descending=False).data:
            x = bar.x[0]
            y = bar.y[0]
            x_to_ys.setdefault(x, []).append(y)
        for ys in x_to_ys.values():
            assert ys == sorted(ys)

    @staticmethod
    def test_sorted_vertical_bars_by_y_values_empty():
        try:
            sorted_vertical_bars_by_y_values(go.Figure())
        except ValueError as e:
            assert str(e) == "No vertical bar traces found in figure."
        else:
            assert False, "Expected ValueError for empty figure"

    @staticmethod
    def test_sorted_vertical_bars_by_y_values_single_bar():
        figure = go.Figure()
        figure.add_bar(x=[1], y=[10], name="A")
        sorted_fig = sorted_vertical_bars_by_y_values(figure)

        assert len(sorted_fig.data) == 1
        assert sorted_fig.data[0].y[0] == 10

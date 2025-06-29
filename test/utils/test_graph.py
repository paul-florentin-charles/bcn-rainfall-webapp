import json

from bcn_rainfall_webapp.utils.graph import (
    aggregate_plotly_json_figures,
    aggregate_plotly_json_pie_charts,
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

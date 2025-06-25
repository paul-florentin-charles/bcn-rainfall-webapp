function sortGraph(
    graph_json,
    graph_div_id,
    order // Should be either 'ascending', 'descending' or ''
) {
    graph_json.layout.xaxis.categoryorder = `total ${order}`.trim();
    Plotly.react(graph_div_id, graph_json, {}, config);
}

function colorizeGraphsFontsOnHover(graph_div_id_to_graph_json) {
    Object.entries(graph_div_id_to_graph_json).forEach(([graph_div_id, graph_json]) => {
        document.getElementById(graph_div_id).addEventListener("mouseover", function () {
            graph_json.layout.font.color = style.getPropertyValue('--link-hover-color');

            Plotly.react(graph_div_id, graph_json, {}, config);
        })

        document.getElementById(graph_div_id).addEventListener("mouseout", function () {
            graph_json.layout.font.color = style.getPropertyValue('--link-color');

            Plotly.react(graph_div_id, graph_json, {}, config);
        })
    })
}

function resizeGraphs(graph_div_id_to_graph_json) {
    ['load', 'resize'].forEach(event => window.addEventListener(event, function () {
        if (window.screen.width < 768) {
            Object.values(graph_div_id_to_graph_json).forEach((graph_json) => {
                graph_json.layout.font.size = 8;
                graph_json.layout.margin = {'t': 65, 'r': 15, 'b': 25, 'l': 25};
            })
        } else {
            Object.values(graph_div_id_to_graph_json).forEach((graph_json) => {
                graph_json.layout.font.size = 11;
                graph_json.layout.margin = {'t': 65, 'r': 30, 'b': 45, 'l': 65};
            })
        }

        Object.entries(graph_div_id_to_graph_json).forEach(([graph_div_id, graph_json]) => {
            Plotly.react(graph_div_id, graph_json, {}, config);
        })
    }))
}
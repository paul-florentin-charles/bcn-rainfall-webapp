const default_layout_dict = {
    'computer': {
        'font_size': 11,
        'margin': {'t': 65, 'r': 30, 'b': 45, 'l': 65}
    },
    'tablet': {
        'font_size': 10,
        'margin': {'t': 65, 'r': 25, 'b': 40, 'l': 55}
    },
    'phone': {
        'font_size': 8,
        'margin': {'t': 65, 'r': 15, 'b': 30, 'l': 25}
    }
}

// {order} should be either 'ascending', 'descending' or ''
function sortGraph(graph_json, graph_div_id, order) {
    graph_json.layout.xaxis.categoryorder = `total ${order}`.trim();
    Plotly.react(graph_div_id, graph_json, {}, config);
}

function colorizeGraphsFontsOnHover(graph_div_id_to_graph_json) {
    Object.entries(graph_div_id_to_graph_json).forEach(([graph_div_id, graph_json]) => {
        colorizeGraphFontsOnHover(graph_div_id, graph_json)
    })
}

function colorizeGraphFontsOnHover(graph_div_id, graph_json) {
    document.getElementById(graph_div_id).addEventListener("mouseover", function () {
        graph_json.layout.font.color = style.getPropertyValue('--link-hover-color');

        Plotly.react(graph_div_id, graph_json, {}, config);
    })

    document.getElementById(graph_div_id).addEventListener("mouseout", function () {
        graph_json.layout.font.color = style.getPropertyValue('--link-color');

        Plotly.react(graph_div_id, graph_json, {}, config);
    })
}

function resizeGraphs(graph_div_id_to_graph_json) {
    ['load', 'resize'].forEach(event => window.addEventListener(event, function () {
        if (window.screen.width < 768) {
            Object.values(graph_div_id_to_graph_json).forEach((graph_json) => {
                graph_json.layout.font.size = default_layout_dict['phone']['font_size'];
                graph_json.layout.margin = default_layout_dict['phone']['margin'];
            })
        } else if (window.screen.width < 1023) {
            Object.values(graph_div_id_to_graph_json).forEach((graph_json) => {
                graph_json.layout.font.size = default_layout_dict['tablet']['font_size'];
                graph_json.layout.margin = default_layout_dict['tablet']['margin'];
            })
        } else {
            Object.values(graph_div_id_to_graph_json).forEach((graph_json) => {
                graph_json.layout.font.size = default_layout_dict['computer']['font_size'];
                graph_json.layout.margin = default_layout_dict['computer']['margin'];
            })
        }

        Object.entries(graph_div_id_to_graph_json).forEach(([graph_div_id, graph_json]) => {
            Plotly.react(graph_div_id, graph_json, {}, config);
        })
    }))
}

function resizeGraph(graph_div_id, graph_json) {
    ['load', 'resize'].forEach(event => window.addEventListener(event, function () {
        if (window.screen.width < 768) {
            graph_json.layout.font.size = default_layout_dict['phone']['font_size'];
            graph_json.layout.margin = default_layout_dict['phone']['margin'];
        } else if (window.screen.width < 1023) {
            graph_json.layout.font.size = default_layout_dict['tablet']['font_size'];
            graph_json.layout.margin = default_layout_dict['tablet']['margin'];
        } else {
            graph_json.layout.font.size = default_layout_dict['computer']['font_size'];
            graph_json.layout.margin = default_layout_dict['computer']['margin'];
        }

        Plotly.react(graph_div_id, graph_json, {}, config);
    }))
}
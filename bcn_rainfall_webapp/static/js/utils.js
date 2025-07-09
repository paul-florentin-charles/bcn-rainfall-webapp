const default_layout_dict = {
    'computer': {
        'font_size': 11,
        'margin': {'t': 75, 'r': 30, 'b': 45, 'l': 65}
    },
    'tablet': {
        'font_size': 10,
        'margin': {'t': 65, 'r': 30, 'b': 35, 'l': 55}
    },
    'phone': {
        'font_size': 8,
        'margin': {'t': 65, 'r': 25, 'b': 25, 'l': 25}
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
    Object.entries({
        'mouseenter': '--link-hover-color',
        'mouseleave': '--link-color'
    }).forEach(([event, cssPropertyName]) => {
        document.getElementById(graph_div_id).addEventListener(event, function () {
            graph_json.layout.font.color = style.getPropertyValue(cssPropertyName);

            Plotly.react(graph_div_id, graph_json, {}, config);
        })
    })
}

function resizeGraphsOnLoadAndResize(graph_div_id_to_graph_json) {
    Object.entries(graph_div_id_to_graph_json).forEach(([graph_div_id, graph_json]) => {
        resizeGraphOnLoadAndResize(graph_div_id, graph_json);
    })
}

function resizeGraphOnLoadAndResize(graph_div_id, graph_json) {
    let device = '';
    ['load', 'resize'].forEach(event => window.addEventListener(event, function () {
        if (window.screen.width < 768) {
            device = 'phone';
        } else if (window.screen.width < 1023) {
            device = 'tablet';
        } else {
            device = 'computer';
        }

        graph_json.layout.font.size = default_layout_dict[device]['font_size'];
        graph_json.layout.margin = default_layout_dict[device]['margin'];

        Plotly.react(graph_div_id, graph_json, {}, config);
    }))
}

function plotGraph(graph_div_id, graph_json) {
    resizeGraphOnLoadAndResize(graph_div_id, graph_json);
    colorizeGraphFontsOnHover(graph_div_id, graph_json);

    let device = ''
    if (window.screen.width < 768) {
        device = 'phone'
    } else if (window.screen.width < 1023) {
        device = 'tablet'
    } else {
        device = 'computer'
    }

    graph_json.layout.font.size = default_layout_dict[device]['font_size'];
    graph_json.layout.margin = default_layout_dict[device]['margin'];

    Plotly.react(graph_div_id, graph_json, {}, config);
}
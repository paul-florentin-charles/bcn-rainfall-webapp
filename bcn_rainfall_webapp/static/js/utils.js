const default_layout_dict = {
    'computer': {
        'font_size': 11,
        'margin': {'t': 75, 'r': 30, 'b': 45, 'l': 65},
        'dragmode': 'zoom',
    },
    'tablet': {
        'font_size': 10,
        'margin': {'t': 65, 'r': 30, 'b': 35, 'l': 55},
        'dragmode': false,
    },
    'phone': {
        'font_size': 8,
        'margin': {'t': 65, 'r': 25, 'b': 25, 'l': 25},
        'dragmode': false,
    }
}

function getDevice() {
    if (window.screen.width < 768) {
        return 'phone'
    } else if (window.screen.width < 1023) {
        return 'tablet'
    } else {
        return 'computer'
    }
}

// {order} should be either 'ascending', 'descending' or ''
function sortGraph(graph_json, graph_div_id, order) {
    graph_json.layout.xaxis.categoryorder = `total ${order}`.trim();

    Plotly.react(graph_div_id, graph_json.data, graph_json.layout);
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

            Plotly.react(graph_div_id, graph_json.data, graph_json.layout);
        })
    })
}

function colorizeGraphWithThemeColors(graph_div_id, graph_json) {
    graph_json.layout.legend.bgcolor = style.getPropertyValue('--legend-background-color');
    graph_json.layout.font.color = style.getPropertyValue('--link-color');
    graph_json.layout.paper_bgcolor = style.getPropertyValue('--header-background-color');
    graph_json.layout.plot_bgcolor = style.getPropertyValue('--background-color');

    Plotly.animate(graph_div_id, {
        layout: graph_json.layout
    }, {
        transition: {
            duration: 300,
            easing: 'ease-in-out'
        },
        frame: {
            duration: 300
        }
    });
}

function colorizeGraphOnLoadAndThemeSwitch(graph_div_id, graph_json) {
    window.addEventListener('load', () => {
        colorizeGraphWithThemeColors(graph_div_id, graph_json);
    });

    document.getElementById('theme-switch').addEventListener('click', () => {
        colorizeGraphWithThemeColors(graph_div_id, graph_json);
    });
}

function colorizeGraphsOnLoadAndThemeSwitch(graph_div_id_to_graph_json) {
    Object.entries(graph_div_id_to_graph_json).forEach(([graph_div_id, graph_json]) => {
        colorizeGraphOnLoadAndThemeSwitch(graph_div_id, graph_json);
    })
}

function resizeGraphsOnLoadAndResize(graph_div_id_to_graph_json) {
    Object.entries(graph_div_id_to_graph_json).forEach(([graph_div_id, graph_json]) => {
        resizeGraphOnLoadAndResize(graph_div_id, graph_json);
    })
}

function resizeGraphOnLoadAndResize(graph_div_id, graph_json) {
    ['load', 'resize'].forEach(event => window.addEventListener(event, function () {
        let device = getDevice();
        graph_json.layout.font.size = default_layout_dict[device]['font_size'];
        graph_json.layout.margin = default_layout_dict[device]['margin'];
        graph_json.layout.dragmode = default_layout_dict[device]['dragmode'];

        Plotly.react(graph_div_id, graph_json.data, graph_json.layout);
    }))
}

function replotGraph(graph_div_id, graph_json) {
    resizeGraphOnLoadAndResize(graph_div_id, graph_json);
    colorizeGraphFontsOnHover(graph_div_id, graph_json);

    let device = getDevice();
    graph_json.layout.font.size = default_layout_dict[device]['font_size'];
    graph_json.layout.margin = default_layout_dict[device]['margin'];
    graph_json.layout.dragmode = default_layout_dict[device]['dragmode'];
    graph_json.layout.legend.bgcolor = style.getPropertyValue('--legend-background-color');
    graph_json.layout.font.color = style.getPropertyValue('--link-color');
    graph_json.layout.paper_bgcolor = style.getPropertyValue('--header-background-color');
    graph_json.layout.plot_bgcolor = style.getPropertyValue('--background-color');

    Plotly.react(graph_div_id, graph_json.data, graph_json.layout);
}

function plotGraphs(graph_div_id_to_graph_json) {
    Object.entries(graph_div_id_to_graph_json).forEach(([graph_div_id, graph_json]) => {
        plotGraph(graph_div_id, graph_json);
    })
}

function plotGraph(graph_div_id, graph_json) {
    graph_json.layout.legend.bgcolor = style.getPropertyValue('--legend-background-color');
    graph_json.layout.font.color = style.getPropertyValue('--link-color');
    graph_json.layout.paper_bgcolor = style.getPropertyValue('--header-background-color');
    graph_json.layout.plot_bgcolor = style.getPropertyValue('--background-color');

    Plotly.newPlot(graph_div_id, graph_json.data, graph_json.layout, default_plotly_config);
}
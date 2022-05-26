// Initilizing Empty Array
var dataList = [];
var nodeList = [];
var endNodeList = [];
var edgeList = [];
var network;

// Creating Neo4J Driver
var driver = neo4j.driver(
    'bolt://localhost:7687/',
    neo4j.auth.basic('neo4j', 'Manju12345')
)

// Start Nei4J Session
var session = driver.session()

// get Data from Neo4J based on Query
function filter(qry) {
    session
        .run(qry)
        .then(result => {
            result.records.forEach(record => {
                //console.log(record)
                dataList.push(record);
            })
        })
        .catch(error => {
            console.log(error)
        })
        .then(() => {
            //console.log(dataList);
            createGraph(dataList);
        })
}

// Create Graph Network
function createGraph(data) {
    //console.log("Record Length => ", data.length);
    var color = 'orange';
    var font = '12px arial black';
    data.forEach((record) => {
        console.log(record);
        // Checking for Organization, Individual, SUPPLY_TO, BUY_FROM, FUND_TO, Green Score etc.
        if (record._fields[0].end.labels[0] == 'Organization') {
            color = {
                background: '#4895ef',
                border: '#3f37c9',
                highlight: {
                    border: '#80ffdb',
                    background: '#0b132b'
                },
            }
            // color = '#4895ef';
            font = '12px arial white';
        } else if (record._fields[0].end.labels[0] == 'Individual') {
            color = {
                background: '#ff477e',
                border: '#c9184a',
                highlight: {
                    border: '#80ffdb',
                    background: '#0b132b'
                },
            }
            font = '12px arial white';

        }

        // Getting Start/Center Node ID, Label, Properties
        var sid = record._fields[0].start.identity.low;
        var slabel = record._fields[0].start.labels[0];
        var sproperties = record._fields[0].start.properties;
        var stitle = sproperties.Org_Name;


        // Check for Start / Center Node
        if (!endNodeList.some((n) => n.id == sid)) {
            var snode = {};
            snode.id = sid;
            snode.label = stitle.substring(0, 9) + "...";
            snode.color = color;
            snode.font = font;
            endNodeList.push(snode);
        }

        // Getting Edge Node/End Node ID, Label and Properties
        var eid = record._fields[0].end.identity.low;
        var elabel = record._fields[0].end.properties.Org_Name;
        var eproperties = record._fields[0].end.properties;
        var etitle = eproperties.Org_Name;

        var enode = {};
        enode.id = eid;
        enode.label = etitle.substring(0, 9) + "...";
        enode.color = color;
        enode.font = font;
        endNodeList.push(enode);

        // var from = record._fields[0].start.identity.low;
        // var to = record._fields[0].segments[0].end.identity.low;
        var from = record._fields[0].segments[0].relationship.start.low;
        var to = record._fields[0].segments[0].relationship.end.low;

        var edgeLabel = record._fields[0].segments[0].relationship.type;



        var edgenode = {};
        edgenode.from = from;
        edgenode.to = to;
        edgenode.width = 1;
        edgenode.length = 200;
        edgenode.label = edgeLabel;
        edgenode.arrows = 'to';
        edgenode.font = { size: 10, align: 'middle', color: 'grey' };
        // edgenode.label = etitle.substring(0, 9) + "...";
        edgeList.push(edgenode);

    });
    setTimeout(drawGraph(), 3000);
}

// Dispay Graph
function drawGraph() {

    console.log(endNodeList);
    console.log(edgeList);

    // create an array with nodes
    var nodes = new vis.DataSet(endNodeList);
    // create an array with edges
    var edges = new vis.DataSet(edgeList);

    // create a network
    var container = document.getElementById("mynetwork");
    var nodedata = {
        nodes: nodes,
        edges: edges,
    };
    var options = {
        nodes: {
            shape: 'circle',
            borderWidth: 5,
            borderWidthSelected: 5,
            shadow: {
                enabled: true,
            }
        },
        edges: {
            color: 'grey',
            font: '10px arial #ff0000',
            scaling: {
                label: false,
            },
            shadow: true,
            // smooth: true,
        }

    };
    var network = new vis.Network(container, nodedata, options);


    network.on('selectEdge', function (properties) {
        var ids = properties.nodes;
        var clickedNodes = nodes.get(ids);
        console.log('clicked edge:', clickedNodes);
    });
    network.on('selectNode', function (properties) {
        var ids = properties.nodes;
        var clickedNodes = nodes.get(ids);
        console.log('clicked nodes:', clickedNodes);
    });
}


var qry = 'MATCH p=(Organization{Org_ID:1})-[]-() RETURN p';
// 'MATCH p=(Organization{Org_ID:1})-[]-() RETURN p';
// 'MATCH p=(Organization {Org_ID:13})-[r:SUPPLY_TO]->() RETURN p'
// MATCH p=(Organization{Org_ID:13})-[r:SUPPLY_TO]->() RETURN p
filter(qry);
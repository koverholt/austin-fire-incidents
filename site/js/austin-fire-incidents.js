var xhr = new XMLHttpRequest();
xhr.open("GET", "https://us-central1-koverholt-apps-304316.cloudfunctions.net/austin-fire-incidents");
xhr.setRequestHeader("Content-Type", "application/json");
xhr.send();

xhr.onload = function () {
  var obj = JSON.parse(this.response);

  function unpack(rows, key) {
    return rows.map(function(row) { return row[key]; });
  }

  var classArray = unpack(obj, 'Problem');
  var classes = [...new Set(classArray)];

  var data = classes.map(function(classes) {
    var rowsFiltered = obj.filter(function(row) {
        return (row.Problem === classes);
    });
    return {
        type: 'scattermapbox',
        name: classes,
        lat: unpack(rowsFiltered, 'Latitude'),
        lon: unpack(rowsFiltered, 'Longitude'),
    };
  });

  var layout = {
    autosize: true,
    hovermode:'closest',
    showlegend: true,
    margin: {
      r: 0,
      t: 0,
      b: 0,
      l: 0,
      pad: 0
    },
    mapbox: {
      style: "carto-positron",
      bearing: 0,
      center: {
        lat: 30.30088,
        lon: -97.7597,
      },
      pitch: 0,
      zoom: 9
    },
  }

  Plotly.newPlot('map', data, layout)

};

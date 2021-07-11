$(".wrapper").delay(600).fadeIn(500);
var barDataset = [
  {
    "date": 1,
    "successful": 1,
    "unsuccessful": 2
  },
  {
    "date": 2,
    "successful": 41,
    "unsuccessful": 8
  },
  {
    "date": 3,
    "successful": 44,
    "unsuccessful": 4
  },
  {
    "date": 4,
    "successful": 2,
    "unsuccessful": 5
  },
  {
    "date": 5,
    "successful": 21,
    "unsuccessful": 1
  },
  {
    "date": 6,
    "successful": 14,
    "unsuccessful": 6
  },
  {
    "date": 7,
    "successful": 42,
    "unsuccessful": 1
  },
  {
    "date": 8,
    "successful": 10,
    "unsuccessful": 1
  },
  {
    "date": 9,
    "successful": 24,
    "unsuccessful": 10
  },
  {
    "date": 10,
    "successful": 23,
    "unsuccessful": 6
  },
  {
    "date": 11,
    "successful": 21,
    "unsuccessful": 15
  },
  {
    "date": 12,
    "successful": 28,
    "unsuccessful": 15
  },
  {
    "date": 13,
    "successful": 40,
    "unsuccessful": 5
  },
  {
    "date": 14,
    "successful": 6,
    "unsuccessful": 12
  },
  {
    "date": 15,
    "successful": 3,
    "unsuccessful": 3
  },
  {
    "date": 16,
    "successful": 6,
    "unsuccessful": 14
  },
  {
    "date": 17,
    "successful": 21,
    "unsuccessful": 2
  },
  {
    "date": 18,
    "successful": 5,
    "unsuccessful": 1
  },
  {
    "date": 19,
    "successful": 21,
    "unsuccessful": 15
  },
  {
    "date": 20,
    "successful": 36,
    "unsuccessful": 14
  },
  {
    "date": 21,
    "successful": 48,
    "unsuccessful": 12
  },
  {
    "date": 22,
    "successful": 26,
    "unsuccessful": 10
  },
  {
    "date": 23,
    "successful": 29,
    "unsuccessful": 15
  },
  {
    "date": 24,
    "successful": 38,
    "unsuccessful": 14
  },
  {
    "date": 25,
    "successful": 11,
    "unsuccessful": 2
  },
  {
    "date": 26,
    "successful": 4,
    "unsuccessful": 11
  },
  {
    "date": 27,
    "successful": 18,
    "unsuccessful": 5
  },
  {
    "date": 28,
    "successful": 40,
    "unsuccessful": 1
  },
  {
    "date": 29,
    "successful": 19,
    "unsuccessful": 7
  },
  {
    "date": 30,
    "successful": 25,
    "unsuccessful": 7
  },
  {
    "date": 31,
    "successful": 15,
    "unsuccessful": 17
  }
]

function drawBarGraph(data) {

  var status = ["successful", "unsuccessful"];

  var colors = [ ["Successful", "#50E3C2"],
                ["Unsuccessful", "#EF5C6E"] ];

  var margin = {top: 30, right: 30, bottom: 40, left: 60},
      width  = 860 - margin.left - margin.right,
      height = 290 - margin.top - margin.bottom;

  var z = d3.scale.ordinal()
  .range(["#50E3C2", "#EF5C6E"]);

  var n = 32;

  var x = d3.scale.linear()
  .domain([1, n - 1])
  .rangeRound([0, width], .1);

  var y = d3.scale.linear()
  .rangeRound([height, 0]);

  var xAxis = d3.svg.axis()
  .scale(x)
  .orient("bottom")
  .tickFormat(d3.format("d"))
  .ticks(30);

  var yAxis = d3.svg.axis()
  .scale(y)
  .orient("left")
  .ticks(5)
  .tickFormat(d3.format("d"));

  var svg = d3.select("#chart-bar")
  .append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
  .append("g")
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  var layers = d3.layout.stack()
  (status.map(function (c) {
    return data.map(function (d) {
      return {x: d.date, y: d[c]};
    });
  }));


  y.domain([
    0, d3.max(layers[layers.length - 1], function (d) {
      return d.y0 + d.y;
    })
  ]);


  // gridlines in y axis function
  function make_y_gridlines() {
    return d3.svg.axis().scale(y)
      .orient("left").ticks(5);
  }

  // add the Y gridlines
  svg.append("g")
    .attr("class", "gridline")
    .call(make_y_gridlines()
          .tickSize(-width)
          .tickFormat("")
         );

  svg.append("g")
    .attr("class", "axis axis--x")
    .attr("transform", "translate(6," + height + ")")
    .call(xAxis)
    .append("text")
    .attr("transform", "translate(364,0)")
    .attr("y", "3em")
    .style("text-anchor", "middle")
    .text("Days");

  svg.append("g")
    .attr("class", "axis axis--y")
    .call(yAxis)
    .append("text")
    .attr("transform", "rotate(-90)")
    .attr("x", "-5em")
    .attr("y", "-2.5em")
    .style("text-anchor", "end")
    .text("Number of calls sent");


  function type(d) {
    // d.date = parseDate(d.date);
    d.date;
    status.forEach(function (c) {
      d[c] = +d[c];
    });
    return d;
  }  
  
  var tooltip = d3.select("#chart-bar").append("div")
  .attr("class", "tooltip")
  .style("opacity", 0);

  var layer = svg.selectAll(".layer")
  .data(layers)
  .enter().append("g")
  .attr("class", "layer")
  .style("fill", function (d, i) {
    return z(i);
  });

  layer.selectAll("rect")
    .data(function (d) {
    return d;
  })
    .enter().append("rect")
    .on("mouseover", function (d) {
    tooltip.transition()
      .duration(200)
      .style("opacity", 1);
    tooltip.html("<span>" + d.y + " calls" + "</span>")
      .style("left", (d3.event.pageX - 25) + "px")
      .style("top", (d3.event.pageY - 28) + "px");
  })
    .on("mouseout", function (d) {
    tooltip.transition()
      .duration(500)
      .style("opacity", 0);
  })
      .attr("x", function (d) {
    return x(d.x);
  })
    .attr("y",  function(d) {
    return height;
  })
    .attr("width", 12)
    .attr("height", 0)
    .transition().duration(1500)
    .attr("y", function (d) {
    return y(d.y + d.y0);
  })
    .attr("height", function (d) {
    return y(d.y0) - y(d.y + d.y0);
  });

}

drawBarGraph(barDataset);


$('.count').each(function () {
  $(this).prop('Counter',0).animate({
    Counter: $(this).text()
  }, {
    duration: 1500,
    easing: 'swing',
    step: function (now) {
      $(this).text(Math.ceil(now));
    }
  });
});
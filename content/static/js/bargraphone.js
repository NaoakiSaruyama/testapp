$(".wrapper").delay(600).fadeIn(500);
var barDataset = [
  {
    "date": 1,
    "total": 1,
  },
  {
    "date": 2,
    "total": 41,
  },
  {
    "date": 3,
    "total": 21,
  },
  {
    "date": 4,
    "total": 41,
  },
  {
    "date": 5,
    "total": 31,
  },
  {
    "date": 6,
    "total": 41,
  },
  {
    "date": 7,
    "total": 41,
  },
  {
    "date": 8,
    "total": 41,
  },
  {
    "date": 9,
    "total": 41,
  },
  {
    "date": 10,
    "total": 81,
  },
  {
    "date": 11,
    "total": 41,
  },
  {
    "date": 12,
    "total": 41,
  },
  {
    "date": 13,
    "total": 41,
  },
  {
    "date": 14,
    "total": 41,
  },
  {
    "date": 15,
    "total": 41,
  },
  {
    "date": 16,
    "total": 41,
  },
  {
    "date": 17,
    "total": 41,
  },
  {
    "date": 18,
    "total": 41,
  },
  {
    "date": 19,
    "total": 41,
  },
  {
    "date": 20,
    "total": 41,
  },
  {
    "date": 21,
    "total": 41,
  },
  {
    "date": 22,
    "total": 41,
  },
  {
    "date": 23,
    "total": 41,
  },
  {
    "date": 24,
    "total": 41,
  },
  {
    "date": 25,
    "total": 41,
  },
  {
    "date": 26,
    "total": 41,
  },
  {
    "date": 27,
    "total": 41,
  },
  {
    "date": 28,
    "total": 41,
  },
  {
    "date": 29,
    "total": 41,
  },
  {
    "date": 30,
    "total": 41,
  },
  {
    "date": 31,
    "total": 41,
  }
]

function drawBarGraph(data) {

  var status = ["total"];

  var colors = ["total", "#50E3C2"];

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
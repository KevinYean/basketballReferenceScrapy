var colorIncrement = -1;

var svg = d3.select("body")
	.append("svg")
	.append("g")

svg.append("g")
	.attr("class", "slices");
svg.append("g")
	.attr("class", "labels");
svg.append("g")
	.attr("class", "lines");

var width = 960,
    height = 450,
	radius = Math.min(width, height) / 2;

var pie = d3.layout.pie()
	.value(function(d) {
		return d.value;
	});

var arc = d3.svg.arc()
	.outerRadius(radius * 0.8)
	.innerRadius(radius * 0.4);

var outerArc = d3.svg.arc()
	.innerRadius(radius * 0.9)
	.outerRadius(radius * 0.9);

svg.attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

var key = function(d){ return d.data.label; };

var dataset1 = [
		{ label: 'Luol Deng', value: 14354067 },
        { label: 'Anthony Tolliver', value: 5750000 },
        { label: 'Keita Bates-Diop', value: 838464 },
        { label: 'Derrick Rose', value: 2176270 },
        { label: 'Josh Okogie', value: 2160720 },
        { label: 'Taj Gibson', value: 14000000 },
        { label: 'Jeff Teague', value: 19000000 },
        { label: 'Jerryd Bayless', value: 8575916 },
        { label: 'Dario Saric', value: 3481986 },
        { label: 'Tyus Jones', value: 244053 },
        { label: 'Karl Anthony Town', value: 7389435 },
        { label: 'Andre Wiggins', value: 25467250 },
        { label: 'Gorgui Dieng', value: 15170787 },
    ];

var dataset2 = [
    { label: "Jamal Crawford", value: 2304226},
    { label: "Devin Booker", value: 3314365}
]





var allDataSets = [dataset1,dataset2]


function randomData (){
    colorIncrement = -1;
    rand = Math.floor(Math.random() *2);
    return allDataSets[rand];
}

change(randomData());

d3.select(".randomize")
	.on("click", function(){
		change(randomData());
	});

function randomColor(d){
	colorIncrement++;
	colorList = ["#fc0505", "#fcae05","#ebfc05", "#9dfc05", "#05fc63",
				"#05fcf0","#5705fc","#9105fc","#fc05d7","#fc0578",
				"#23562d","#234656","#247093","#7cea54","#cc942c"];
    return colorList[colorIncrement];
}

function change(data) {

	/* ------- PIE SLICES -------*/
	var slice = svg.select(".slices").selectAll("path.slice")
		.data(pie(data), key);

	slice.enter()
		.insert("path")
		.style("fill", function(d) { return randomColor(d); })
		.attr("class", "slice");

	slice		
		.transition().duration(1000)
		.attrTween("d", function(d) {
			this._current = this._current || d;
			var interpolate = d3.interpolate(this._current, d);
			this._current = interpolate(0);
			return function(t) {
				return arc(interpolate(t));
			};
		})

	slice.exit()
		.remove();

	/* ------- TEXT LABELS -------*/

	var text = svg.select(".labels").selectAll("text")
		.data(pie(data), key);

	text.enter()
		.append("text")
		.attr("dy", ".35em")
		.text(function(d) {
			return d.data.label;
		});
	
	function midAngle(d){
		return d.startAngle + (d.endAngle - d.startAngle)/2;
	}

	text.transition().duration(1000)
		.attrTween("transform", function(d) {
			this._current = this._current || d;
			var interpolate = d3.interpolate(this._current, d);
			this._current = interpolate(0);
			return function(t) {
				var d2 = interpolate(t);
				var pos = outerArc.centroid(d2);
				pos[0] = radius * (midAngle(d2) < Math.PI ? 1 : -1);
				return "translate("+ pos +")";
			};
		})
		.styleTween("text-anchor", function(d){
			this._current = this._current || d;
			var interpolate = d3.interpolate(this._current, d);
			this._current = interpolate(0);
			return function(t) {
				var d2 = interpolate(t);
				return midAngle(d2) < Math.PI ? "start":"end";
			};
		});

	text.exit()
		.remove();

	/* ------- SLICE TO TEXT POLYLINES -------*/

	var polyline = svg.select(".lines").selectAll("polyline")
		.data(pie(data), key);
	
	polyline.enter()
		.append("polyline");

	polyline.transition().duration(1000)
		.attrTween("points", function(d){
			this._current = this._current || d;
			var interpolate = d3.interpolate(this._current, d);
			this._current = interpolate(0);
			return function(t) {
				var d2 = interpolate(t);
				var pos = outerArc.centroid(d2);
				pos[0] = radius * 0.95 * (midAngle(d2) < Math.PI ? 1 : -1);
				return [arc.centroid(d2), outerArc.centroid(d2), pos];
			};			
		});
	
	polyline.exit()
		.remove();
};
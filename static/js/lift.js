$("#startlocation").autocomplete({
    minLength: 1,
    source: function (request, response, url) {
        var searchParam = request.term;
        $.ajax({
            url: '/get_addr/?search=' + request.term,
            data: searchParam,
            dataType: "json",
            type: "GET",
            cache: true,
            success: function (data) {
                response($.map(data, function (item, index) {
                    return {
                        label: item,
                        value: item,
                        nodeid: index
                    };
                }));
            }
        });//ajax ends
    },
    select: function (a, b) {
        $("#hiddenstart").val(b.item.nodeid);
        // Appends an array with 2 keys: Value and Label.
        // Both display the title and date as shown above.
    }
}).data("ui-autocomplete")._renderItem = function (ul, item) {
    const htmlstring = `<li class="ui-menu-item"><div class="ui-menu-item-wrapper" tabindex="-1"></div></li>`;
    const $li = $(htmlstring);
    const id = $(ul).find('li').length + 1;
    $li.find('div').attr("data-id", item.nodeid).attr("id", id).html(item.label);
    return $li.appendTo(ul);
};

$("#endlocation").autocomplete({
    minLength: 1,
    source: function (request, response, url) {
        var searchParam = request.term;
        $.ajax({
            url: '/get_addr/?search=' + request.term,
            data: searchParam,
            dataType: "json",
            type: "GET",
            cache: true,
            success: function (data) {
                response($.map(data, function (item, index) {
                    return {
                        label: item,
                        value: item,
                        nodeid: index
                    };
                }));
            }
        });//ajax ends
    },
    select: function (a, b) {
        $("#hiddenend").val(b.item.nodeid);
    }
}).data("ui-autocomplete")._renderItem = function (ul, item) {
    const htmlstring = `<li class="ui-menu-item"><div class="ui-menu-item-wrapper" tabindex="-1"></div></li>`;
    const $li = $(htmlstring);
    const id = $(ul).find('li').length + 1;
    $li.find('div').attr("data-id", item.nodeid).attr("id", id).html(item.label);
    return $li.appendTo(ul);
};
// For Map

// Map Marker on select
$(document).on('click', '.mapboxgl-marker', function () {
    var node_id = $("#nodeidhidden");
    var node_text = $('#nodebuilding');
    $("#hiddenstart").val(node_id.text());
    $("#startlocation").val(node_text.text());
});
const speedFactor = 30; // number of frames per longitude degree
let animation; // to store and cancel the animation
var route_counter = 1;


// $("#searchbtn").click(function () {
//     var startloc = $("#hiddenstart").val();
//     var endloc = $("#hiddenend").val();
//     $.ajax({
//         type: "POST",
//         url: "/getPrice/",
//         data: {
//             csrfmiddlewaretoken: "{{csrf_token}}",
//             starting: startloc,
//             ending: endloc,
//             //price: $('input[name="rideprice"]').val(),
//         },
//         success: function (result) {
//             //   $("#result").html("<h2>Received!</h2>");
//             $("#price").val(result);
//
//             if (confirm("Price Of Fare " + result + "\n Click OK to confirm ride")) {
//                 // getInfo();
//             }
//             document.getElementById("accept").innerHTML = result;
//         },
//     });
//     $.ajax({
//         reply: false,
//         type: "POST",
//         url: "/bookingsearch/",
//         data: {
//             csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
//             starting: startloc,
//             ending: endloc,
//             //price: $('input[name="rideprice"]').val(),
//         },
//         success: function (data) {
//             var geojson = {
//                 'type': 'FeatureCollection',
//                 'features': [
//                     {
//                         'type': 'Feature',
//                         'geometry': {
//                             'type': 'LineString',
//                             'coordinates': [data['coordinates'][0]]
//                         }
//                     }
//                 ]
//             };
//             map.addSource("route", {
//                 'type': "geojson",
//                 'data': geojson
//             });
//
//             map.addLayer({
//                 id: "line-animation",
//                 type: "line",
//                 source: "route",
//                 layout: {
//                     "line-join": "round",
//                     "line-cap": "round",
//                 },
//                 paint: {
//                     "line-color": "#ee2323",
//                     "line-width": 8,
//                 },
//             });
//
//             animateLine();
//
//             function animateLine() {
//                 // append new coordinates to the lineString
//                 if (route_counter !== data['coordinates'].length) {
//                     geojson.features[0].geometry.coordinates.push(data['coordinates'][route_counter]);
//                     // then update the map
//                     route_counter++;
//                     map.getSource('route').setData(geojson);
//                     // Request the next frame of the animation.
//                     animation = requestAnimationFrame(animateLine);
//                 }
//
//             }
//         },
//     });
// });

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
if ("geolocation" in navigator) {
    navigator.geolocation.getCurrentPosition(position => {

        map = new mapboxgl.Map({
            container: "map",
            pitch: 45,
            center: [position.coords.longitude, position.coords.latitude],
            zoom: 17, // starting zoom
            style: "mapbox://styles/exkingist/cl0s7xq5v001i14n5vioj61u5",
        });
        $.ajax({
            type: "GET",
            url: "/findnearest/",
            cache: true,
            data: {
                'lat': position.coords.latitude,
                'long': position.coords.longitude
            }, success: function (result) {
                const data = JSON.parse(result["data"]);
                console.log(data);
                for (var i = 0; i < data.length; i++) {
                    var obj = data[i];
                    if (obj.POSTALCODE === 'NIL') {
                        var marker = new mapboxgl.Marker()
                            .setLngLat([obj.long, obj.lat])
                            .setPopup(new mapboxgl.Popup().setHTML("<h id='nodebuilding'>" + obj.BUILDINGNAME + "</h><p id='nodeidhidden' class='d-none'>" + obj.id + "</p>"))
                            .addTo(map);
                    } else {
                        var marker = new mapboxgl.Marker()
                            .setLngLat([obj.long, obj.lat])
                            .setPopup(new mapboxgl.Popup().setHTML("<h id='nodebuilding'>" + obj.BUILDINGNAME + "</h><p> " + obj.POSTALCODE + "</p> <p  id='nodeidhidden'  class='d-none'>" + obj.id + "</p>"))
                            .addTo(map);
                    }


                }
            }
        });
        map.addControl(new mapboxgl.NavigationControl(), 'bottom-left');
        const geolocate = new mapboxgl.GeolocateControl({
            positionOptions: {
                enableHighAccuracy: true,
            },
            trackUserLocation: true
        });
        map.addControl(geolocate, 'bottom-left');

        // Used to Get lat and longitude coordinates
        // TODO: USE THIS LOCATION when user press.
        geolocate.on('geolocate', function (position) {
            latitude = position.coords.latitude;
            longitude = position.coords.longitude;
        });


        map.on('load', () => {
            // Insert the layer beneath any symbol layer.
            map.resize();
            const layers = map.getStyle().layers;
            const labelLayerId = layers.find(
                (layer) => layer.type === 'symbol' && layer.layout['text-field']
            ).id;

            // The 'building' layer in the Mapbox Streets
            // vector tileset contains building height data
            // from OpenStreetMap.
            map.addLayer(
                {
                    'id': 'add-3d-buildings',
                    'source': 'composite',
                    'source-layer': 'building',
                    'filter': ['==', 'extrude', 'true'],
                    'type': 'fill-extrusion',
                    'minzoom': 15,
                    'paint': {
                        'fill-extrusion-color': '#aaa',
                        // Use an 'interpolate' expression to
                        // add a smooth transition effect to
                        // the buildings as the user zooms in.
                        'fill-extrusion-height': [
                            'interpolate',
                            ['linear'],
                            ['zoom'],
                            15,
                            0,
                            15.05,
                            ['get', 'height']
                        ],
                        'fill-extrusion-base': [
                            'interpolate',
                            ['linear'],
                            ['zoom'],
                            15,
                            0,
                            15.05,
                            ['get', 'min_height']
                        ],
                        'fill-extrusion-opacity': 0.6
                    }
                },
                labelLayerId
            );
            map.resize();
        });


    });
}


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

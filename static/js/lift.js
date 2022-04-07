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

$(".typechoice").on('click', function () {
    if ($(this).attr('id') === "fiveseaterchoice") {
        $("#typeofride").attr("data-lift-ridetype", "5 Seater");
    } else if ($(this).attr('id') === "eightseaterchoice") {
        $("#typeofride").attr("data-lift-ridetype", "8 Seater");
    } else if ($(this).attr('id') === "sharedchoice") {
        $("#typeofride").attr("data-lift-ridetype", "Shared Rides");
    }
    $("#typeofride").html($(this).html());
});

$("#farecancel").click(function () {
    $('#faremodal').modal('hide');
});


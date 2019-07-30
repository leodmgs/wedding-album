
$(document).ready(function() {
    $(".card-img-top").click(function() {
        $("#modal-image").attr("src", $(this).attr("src"));
        $("#photoModal").modal("show");
    });
    $(".dropdown-item").click(function() {
        var op = $(this).attr("id");
        if (op == "sort-newest" || op == "sort-oldest" || op == "sort-rating") {
            $("#sort-anchor").text("Sort by: " + $(this).text());
            var api_url = $("#sort-anchor").data("api");
            $.get(api_url, { sort: $(this).text()});
        }
    });
});

function add_like(id, url) {
    id_span = '#counter-like-' + id;
    is_liked = $(id_span).hasClass("liked");
    if (!is_liked) {
        $(id_span).html(parseInt($(id_span).html(), 10) + 1);
        $(id_span).removeClass('unliked');
        $(id_span).addClass('liked');
        $('#btn-like-' + id).addClass('liked');
        $.ajax({ url: url + "/like/" + id });
    }
}


$('.fa-comment').click(function(event) {
    var p = $(event.target).closest("article");
    var post_id = p.attr("data-post-id");
    $("#comment_modal").modal('show');
    $(function(){
        $('#comment-form-submit').on('click', function(e) {
            var content = $('#comment_text').val();
            $.ajax({
                type: "POST",
                url: "/post/comment/"+post_id,
                data: {"content":content},
                success: function(response) {
                    var element = p.find(".approve-count-comment");
                    var approve_count = data.count;
                    element.text(approve_count);
                },
                error: function() { 
                }
            });
        });
    });
});

$('.fa-heart').click(function(event) {
        var p = $(event.target).closest("article");
        var post_id = p.attr("data-post-id");
        $.ajax({
        url : "/post/" +post_id+ "/likeAction",
        type: "POST",
        data : {target_type: "post"},
        success: function(data, textStatus, jqXHR)
        {
            console.log(data);
            var element = p.find(".approve-count-heart");
            var approve_count = data.count;
            element.text(approve_count);

        },
        error: function (jqXHR, textStatus, errorThrown)
        {}
        });
});
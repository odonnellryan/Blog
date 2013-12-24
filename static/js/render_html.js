$(function () {
    $('#post_body').on('change keyup paste mouseup',
        function () {
            $.getJSON($SCRIPT_ROOT + '/admin/_render_temp_body/', {
                    post_body: $('textarea[name="post_body"]').val()},
                function (data) {
                    $('#render_body').html(data.result);
                });
            if($('textarea[name="post_body"]').val() == "") {
                $('#render_body').html("");
            }
            return false;
        });

    $('#post_title').on('change keyup paste mouseup',
        function () {
            $('#render_title').html($('input[name="post_title"]').val());
            if($('input[name="post_title"]').val() == "") {
                $('#render_title').html("");
            }
            return false;
        });
});
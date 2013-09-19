$(function() {

  $('#post_body').keyup(
      function() {
            $.getJSON($SCRIPT_ROOT + '/admin/_render_temp_body', {
            post_body: $('textarea[name="post_body"]').val()},
            function(data) {
            $('#render_body').html(data.result);
            });
            return false;
       });

  $('#post_title').keyup(
        function() {
            $.getJSON($SCRIPT_ROOT + '/admin/_render_temp_title', {
            post_title: $('input[name="post_title"]').val()},
            function(data) {
            $('#render_title').html(data.result);
            });
            return false;
        });
});
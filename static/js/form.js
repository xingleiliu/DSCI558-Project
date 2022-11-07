$(document).ready(function() {
    $('form').on('submit', function(event) {
        $('#artist_details').hide();
//        $('#json_container').hide();
        $('#loading').show();
        $.ajax({
            data : {
                job_title: $('#titleInput').val()
            },
            type: 'GET',
            url : '/process'
        })
        .done(function(data) {
            if (data.error) {
                $('#errorAlert').text(data.error).show();
                $('#json_container').hide();
            }
            else {
//                $('#successAlert').text(data.name).show();
                var jsonContainer = document.getElementById("json_container")
                var htmlString = "";
                for (i=0; i < data.length; i++) {
                    // htmlString += "<a href=\"/" + data[i]['id'] + "\">"
                    // htmlString += "<div class=\"empty_bar\">"
                    // artist_id = data[i]['id']
                    htmlString += "<a href=\"javascript:display_artist_info(&quot;" + String(data[i]['id']) + "&quot;);\">";
                    htmlString += "<div class=\"card\" id=\"" + String(data[i]['id']) + "\">";
                    htmlString += "<div class=\"card-body\">";
                    htmlString += "<h5 class=\"card-title\">" + data[i]['job_title'] + "</h5>";
                    htmlString += "</div>";
                    htmlString += "</div></a>";
                }
                // jsonContainer.insertAdjacentHTML('beforeend', htmlString);
                jsonContainer.innerHTML = htmlString;
                $('#errorAlert').hide();
                $('#json_container').show();
            }
            $('#loading').hide();
        });

        event.preventDefault();
    });
});
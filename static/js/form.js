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
                    htmlString += "<div class=\"card\">";
                    htmlString += "<div class=\"card-header\">";
                    htmlString += "<a data-bs-toggle=\"collapse\" data-bs-target=\"#id" + String(i) + "\">";
                    htmlString += "<h5 class=\"card-title\">" + data[i]['job_title'] + "</h5>";
                    htmlString += "<h6 class=\"card-subtitle mb-2 text-muted\">" + data[i]['company'] + "</h6>";
                    htmlString += "</a>";
                    htmlString += "</div>";
                    htmlString += "<div id=\"id" + String(i) + "\" class=\"collapse\" data-bs-parent=\"#json_container\">";
                    htmlString += "<div class=\"card-body\">Company Information<br>Job Descriptions<br>Similar Jobs: </div>"
                    htmlString += "</div>";
                    htmlString += "</div>";
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
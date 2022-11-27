$(document).ready(function() {
    $("#multiselect").multiselect({
    templates: {
      button: '<button type="button" class="multiselect dropdown-toggle btn" data-toggle="dropdown" data-bs-toggle="dropdown" aria-expanded="false"><span class="multiselect-selected-text"></span></button>',
    },
    buttonText: function(options, select) {
                if (options.length === 0) {
                    return '    Skills    ';
                }
                else if (options.length > 3) {
                    return 'More than 3 skills selected!';
                }
                 else {
                     var labels = [];
                     options.each(function() {
                         if ($(this).attr('label') !== undefined) {
                             labels.push($(this).attr('label'));
                         }
                         else {
                             labels.push($(this).html());
                         }
                     });
                     return labels.join(', ') + '';
                 }
            }
  });
    $('form').on('submit', function(event) {
        $('#artist_details').hide();
//        $('#json_container').hide();
        $('#loading').show();
        $.ajax({
            data : {
                job_title: $('#titleInput').val(),
                location: $('#locationInput').val(),
                company: $('#companyInput').val()
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
                    htmlString += "<h5 class=\"card-title\">" + data[i]['title'] + "</h5>";
                    htmlString += "<h6 class=\"card-subtitle mb-2 text-muted\">" + data[i]['company'] + "</h6>";
                    htmlString += "<h6 class=\"card-subtitle mb-2 text-muted\">" + data[i]['location'] + "</h6>";
                    htmlString += "<div>";
                    var skills = ["Python", "Machine Learning", "Sponsor", "2+ years of experience", "$65,000.00 - $160,000.00 per year"];
                    for (var s in skills) {
                        htmlString += "<span class=\"badge bg-primary\">" + skills[s] + "</span>&nbsp;";
                    }
                    htmlString += "</div>";
                    htmlString += "</a>";
                    htmlString += "</div>";
                    // details
                    htmlString += "<div id=\"id" + String(i) + "\" class=\"collapse\" data-bs-parent=\"#json_container\">";
                    htmlString += "<div class=\"card-body\">";
                    htmlString += "<b>Full Job Description</b>";
                    description = data[i]['description'].split("\n");
                    for(var line in description){
                        htmlString += "<p>" + description[line] + "</p>";
                    }
                    htmlString += "</div>";
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
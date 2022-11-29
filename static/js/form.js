$(document).ready(function() {
    $("#multiselect").multiselect({
    enableFiltering: true,
    maxHeight: 450,
    templates: {
      button: '<button type="button" class="multiselect dropdown-toggle btn btn-light" data-toggle="dropdown" data-bs-toggle="dropdown" aria-expanded="false"><span class="multiselect-selected-text"></span></button>',
    },
    buttonText: function(options, select) {
                if (options.length === 0) {
                    return '           Skills         ';
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
                    htmlString += "<h6 class=\"card-subtitle mb-2 text-muted\">" + data[i]['salary'] + "</h6>";
                    htmlString += "<div>";
                    var other_skills = "";
                    var skills = data[i]['qualifications'].split("\n");
                    for (var s in skills) {
                        if (skills[s].length <= 40) {
                            htmlString += "<span class=\"badge bg-secondary\">" + skills[s] + "</span>&nbsp;";
                        }
                        else {
                            other_skills += "<p>" + skills[s].charAt(0).toUpperCase() + skills[s].slice(1) + "</p>";
                        }
                    }
                    htmlString += "</div>";
                    htmlString += "</a>";
                    htmlString += "</div>";
                    // details
                    htmlString += "<div id=\"id" + String(i) + "\" class=\"collapse\" data-bs-parent=\"#json_container\">";
                    htmlString += "<div id=\"description\" class=\"card-body\">";
                    htmlString += "<ul class=\"nav nav-tabs\"";
                    htmlString += "<li class=\"nav-item\">";
                    htmlString += "<a class=\"nav-link active\">Detailed Qualifications</a></li>";
                    htmlString += "<li class=\"nav-item\">";
                    htmlString += "<a class=\"nav-link\">Company Information</a>";
                    htmlString += "</li></ul><br>";
//                    htmlString += "<b>Other Requirements</b>";
                    htmlString += other_skills;
//                    description = data[i]['description'].split("\n");
//                    for(var line in description){
//                        htmlString += "<p>" + description[line] + "</p>";
//                    }
                    htmlString += "</div>";
                    htmlString += "</div>";
                    htmlString += "</div>";
                }
                // jsonContainer.insertAdjacentHTML('beforeend', htmlString);
                jsonContainer.innerHTML = htmlString;
//                var full_description = document.getElementById("description");
//                full_description.innerHTML = other_skills;
                $('#errorAlert').hide();
                $('#json_container').show();
            }
            $('#loading').hide();
        });

        event.preventDefault();
    });
});
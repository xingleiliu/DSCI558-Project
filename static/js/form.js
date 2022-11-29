function display_company_info(company, id) {
//    console.log(company);
//    console.log(id);
    var other_id = "#other" + id;
    $(other_id).hide();
    var company_id = "#company" + id;
    $.ajax({
        data : {
            company: company
        },
        type: 'GET',
        url : '/company'
    })
    .done(function(data) {
        var company_info = JSON.parse(data);
        var company_string = "";
        if (company_info['Description']) {
            company_string += "<p><b>Description: </b>" + company_info['Description'] + "</p>";
        }
        if (company_info['Industries']) {
            company_string += "<p><b>Industries: </b>";
            for (var industry in company_info['Industries']) {
                company_string += "<span class=\"badge bg-primary\">" + company_info['Industries'][industry] + "</span>&nbsp;"
            }
            company_string += "</p>";
        }
        if (company_info['Number of Employees']) {
            company_string += "<p><b>Number of Employees: </b>" + company_info['Number of Employees'] + "</p>";
        }
        if (company_info["Headquarter Location"]) {
            company_string += "<p><b>Headquarter Location: </b>" + company_info['Headquarter Location'] + "</p>";
        }
        if (company_info['Company Website']) {
            company_string += "<p><b>Company Website: </b><a href=\"https://" + company_info['Company Website'].replace(/\s/g, '') + "\">" + company_info['Company Website'] + "</a></p>";
        }
        if (company_info['Founded Date']) {
            company_string += "<p><b>Founded Date: </b>" + company_info['Founded Date'] + "</p>";
        }
        if (company_info['Operating Status']) {
            company_string += "<p><b>Operating Status: </b>" + company_info['Operating Status'] + "</p>";
        }
        if (company_info['Last Funding Type']) {
            company_string += "<p><b>Last Funding Type: </b>" + company_info['Last Funding Type'] + "</p>";
        }
        if (company_info['Related Hubs']) {
            company_string += "<p><b>Related Hubs: </b>" + company_info['Related Hubs'] + "</p>";
        }
        $(company_id).html(company_string);
//        console.log(typeof data);
    });
}




$(document).ready(function() {
//    $( '.nav-tabs' ).on( 'click', function () {
//	$( '.nav-item' ).find( 'li.active' ).removeClass( 'active' );
//	$( this ).parent( 'li' ).addClass( 'active' );
//    });
//    $( ".nav-item" ).on( "click", function() {
//        event.preventDefault();
//        var clickedItem = $( this );
//        $( ".nav-item" ).each( function() {
//            $( this ).removeClass( "active" );
//        });
//        clickedItem.addClass( "active" );
//    });

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
                        skills[s] = skills[s].charAt(0).toUpperCase() + skills[s].slice(1)
                    }
                    skills = [...new Set(skills)];
                    for (var s in skills) {
                        if (skills[s].length <= 40) {
                            htmlString += "<span class=\"badge bg-secondary\">" + skills[s] + "</span>&nbsp;";
                        }
                        else {
                            other_skills += "<p>" + skills[s] + "</p>";
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
                    htmlString += "<a class=\"nav-link\">Detailed Qualifications</a></li>";
                    htmlString += "<li class=\"nav-item\">";
                    htmlString += "<a class=\"nav-link\" href=\"javascript:display_company_info(&quot;" + String(data[i]['company']) + "&quot;," + String(i) + ");\">Company Information</a></li>";
                    htmlString += "<li class=\"nav-item\">";
                    htmlString += "<a class=\"nav-link\">Similar Jobs</a></li>";
                    htmlString += "</ul><br>";
//                    htmlString += "<b>Other Requirements</b>";
                    htmlString += "<div id=\"other" + String(i) + "\">";
                    htmlString += other_skills;
                    htmlString += "</div>";
                    htmlString += "<div id=\"company" + String(i) + "\">"
                    htmlString += "</div>"
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
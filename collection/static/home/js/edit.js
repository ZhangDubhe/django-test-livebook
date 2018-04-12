function loadTopicList() {
    $.post(
        API_PATH + "load-topic",
        {
            csrfmiddlewaretoken: CSRFTOKEN,
            user: session.uuid
        }, function (res) {
            res = JSON.parse(res);
            if (res.status == 20) {
                res.result.forEach(function (topic) {
                    let insertText = '<li id="topiclist-' + topic.id + '" class="list-group-item" onclick="loadDiseaseGroup(this)">' + topic.name + '</li>';
                    $('#topic-list').append(insertText);
                });
            } else {
                layer.msg("[" + res.status + "]" + res.result);
            }
        }
    )
}

function addTopic() {
    var topicName = $('#add-topic-input').val();
    $.post(
        API_PATH + "add-topic",
        {
            csrfmiddlewaretoken: CSRFTOKEN,
            user: session.uuid,
            topic: topicName,
        }, function (res) {
            res = JSON.parse(res);
            console.log(res);
            if (res.status == 20) {
                res.result.forEach(function (topic) {
                    let insertText = '<li id="topiclist-' + topic.id + '" class="list-group-item" onclick="loadDiseaseGroup(this)">' + topic.name + '</li>';
                    $('#topic-list').append(insertText);
                });
            } else {
                layer.msg("[" + res.status + "]" + res.result);
            }
        }
    )
}

function loadDiseaseGroup(object) {
    console.log(object.id);
    $("#disease-group-list").show();
    var topic = object.id.split("-")[1];
    $('#disease-group').html('');
    $.post(
        API_PATH + "load-diseaseGroup",
        {
            csrfmiddlewaretoken: CSRFTOKEN,
            topic: topic
        }, function (res) {
            res = JSON.parse(res);
            if (res.status == 20) {
                console.log(res.result, res.result.length)
                if (res.result.length > 0){
                    res.result.forEach(function (disease) {
                        let insertText = '<li id="diseaseGroup-' + disease.id + '" class="list-group-item" >' + disease.name + '</li>';
                        console.log(insertText);
                        $('#disease-group').append(insertText);
                    });
                } else{
                    $('#disease-group').html('<li class="list-group-item">No result.</li>');
                }
                $('#disease-group').attr('name', res.topicName);
                $('#disease-group-header').html(res.topicName);
                $('#disease-group-header').attr('topic-id',res.topicId);
            } else {
                layer.msg("[" + res.status + "]" + res.result);
            }
        }
    )
}

function searchDisease(type) {
    $("#disease-list-list").show();
    var str = $("#search-disease-input").val();
    console.log(str, type);
    status = 0;
    $("#disease-list").html("<p>searching...</p>");
    if (str.length <= 1 || str == "" || str == " ") {
        if (str == "" || str == " ") $("#disease-list").html("<p></p>");
        return;
    }
    else {
        var url = API_PATH + "search-terms";
        $.getJSON(url, { "str": str, "type": type }, function(res){
            $("#disease-list").html("");
            if (res.status == 20) {
                res.results.forEach(function (disease) {
                    let insertText = '<li id="disease-' + disease.id + '" class="list-group-item" data-toggle="list" role="tab">' + disease.name + '</li>';
                    $("#disease-list").append(insertText);
                });
            } else {
                $("#disease-list").html("<li class='list-group-item'>No result.</li>");
                layer.msg("[" + res.status + "]" + res.result);
            }
        });
    }
}

function addDiseaseToGroup() {
    var topic = $('#disease-group-header').attr('topic-id');
    console.log(topic);

    if(!topic){
        layer.msg("Please select a topic");
        return;
    }
    // LIST OR SINGLE
    var selectDiseaseList = $("#disease-list li.active");
    var diseases = [];
    for (let index = 0; index < selectDiseaseList.length; index++) {
        const selectDisease = selectDiseaseList[index];
        let data = {};
        data.id = $(selectDisease).attr('id').split("-")[1];
        data.name = $(selectDisease).html();
        console.log(data);
        diseases[index] = data;
    }
    console.log(diseases);
    if (diseases.length<=0) {
        layer.msg("Please select disease in disease list");
        return;
    }
    diseases = JSON.stringify(diseases);
    $.post(
        API_PATH + "add-disease-to-group",
        {
            csrfmiddlewaretoken: CSRFTOKEN,
            topic: topic,
            diseases: diseases,
        }, function (res) {
            
            res = JSON.parse(res);
            if (res.status == 20) {
                res.result.forEach(function (disease) {
                    let insertText = '<li id="diseaseGroup-' + disease.id + '" class="list-group-item">' + disease.name + '</li>';
                    $('#disease-group').append(insertText);
                });
                layer.msg("Add successfully.");
            } else {
                layer.msg("[" + res.status + "]" + res.result);
            }
        }
    )
}

function addDisease() {
    var cui = $("#modal-cui").val();
    var name = $("#modal-disease").val();
    console.log(cui, name);
    $.post(
        API_PATH + "add-disease",
        {
            csrfmiddlewaretoken: CSRFTOKEN,
            disease_cui: cui,
            disease_name: name
        }, function (res) {
            res = JSON.parse(res);     
            if (res.status == 20) {
                layer.msg(res.result + " Click x to close the modal window.");    
            } else{
                layer.msg(res.result + " Try again?")
            }
        });
}

function loadTopicList() {
    $.post(
        API_PATH + "load-topic",
        {
            csrfmiddlewaretoken: CSRFTOKEN,
            user: session.uuid
        }, function (res) {
            res = JSON.parse(res);
            if (res.status == 20) {
                console.log(res.result);
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
    var name = $('add-topic-input').val();
    $.post(
        API_PATH + "add-topic",
        {
            csrfmiddlewaretoken: CSRFTOKEN,
            user: session.uuid,
            name: name
        }, function (res) {
            res = JSON.parse(res);
            if (res.status == 20) {
                console.log(result);
                res.result.forEach(function (topic) {
                    let insertText = '<li id="disease-' + topic.id + '" class="list-group-item" onclick="loadDiseaseGroup(this)">' + topic.name + '</li>';
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
    var topic = object.id.split("-")[1];
    console.log(topic);
    $.post(
        API_PATH + "load-diseaseGroup",
        {
            csrfmiddlewaretoken: CSRFTOKEN,
            topic: topic
        }, function (res) {
            res = JSON.parse(res);
            console.log(res);
            if (res.status == 20) {
                res.result.forEach(function (disease) {
                    let insertText = '<li id="disease-' + disease.id + '" class="list-group-item" >' + disease.name + '</li>';
                    console.log(insertText);
                    $('#disease-group').append(insertText);
                });
                $('#disease-group').attr('name', res.topicName);
            } else {
                layer.msg("[" + res.status + "]" + res.result);
            }
        }
    )
}
function addDiseaseToGroup() {
    console.log(object.id);
    var topic = $("#disease-group").attr('name');
    // LIST OR SINGLE
    var disease = '';
    $.post(
        API_PATH + "add-disease-to-group",
        {
            csrfmiddlewaretoken: CSRFTOKEN,
            topic: topic,
            disease: disease
        }, function (res) {
            res = JSON.parse(res);
            if (res.status == 20) {
                res.results.forEach(function (topic) {
                    let insertText = '<li id="disease-' + topic.id + '" class="list-group-item" onclick="loadQuestionGroup(this)">' + topic.name + '</li>';
                    $('#disease-gorup').append(insertText);
                });
            } else {
                layer.msg("[" + res.status + "]" + res.result);
            }
        }
    )
}
function addDisease(cui, name) {
    $.post(
        API_PATH + "add-disease",
        {
            csrfmiddlewaretoken: CSRFTOKEN,
            topic: topic,
            disease: disease
        }, function (res) {
            res = JSON.parse(res);
            layer.msg("[" + res.status + "]" + res.result);          
            
            if (res.status == 20) {
                          
            } 
        })
}
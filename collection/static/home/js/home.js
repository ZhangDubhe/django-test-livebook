function get_def_umls(cui) {
    var tgt = session['tgt'];
    var st = "loop";
    if(tgt){
        console.log("from session:");
        get_st_from_UMLS(tgt);
        st = serviceTicket;
    } else {
        console.log("from Auth:");
        st = get_api_from_UMLS();
    }
    if(status != 200){
        return
    }
    url = "https://uts-ws.nlm.nih.gov/rest/content/current/CUI/"+cui+"/definitions";
    $.getJSON(url, {"ticket":st},function (res) {
        var result = res.result[0];
        var def = result.value;
        $("#disease-def").html(def);
    }).fail(function () {
        $("#disease-def").html("Sorry, there is no defination about this disease.");
    });
}
function add_symptom(){
    var text = $("#input-disease").val();
    $(".selected-ans").append("<button class='btn btn-info mr-2 mb-2 ans-btn' >"+ text +"</button>");
}


function get_api_from_UMLS(){

    $.post(
        API_PATH + "umls_auth",
        {
            name:"Auth",
            csrfmiddlewaretoken:CSRFTOKEN
        },
        function (data) {
            data = JSON.parse(data);
            var result = data["result"];
            if (data["status"] === 200) {
                var serviceTicket = result;
                session.setItem('tgt',data["tgt"]);
                status = 200;
                return serviceTicket;
            }
            else {
                $("#api-response").html(data.result);
            }
        }
    );
}

function get_st_from_UMLS(tgt) {
    params = {'service': "http://umlsks.nlm.nih.gov"}
    $.ajax({
        url:tgt,
        data:params,
        type:"post",
        async:false,
        success:function (data) {
            console.log("res:",data);
            status = 200;
            serviceTicket = data;
            return serviceTicket
    }});
}

function next_question(){
    $.post(API_PATH + "next_quiz",{
            uuid:"1",
            name:"Auth",
            csrfmiddlewaretoken:CSRFTOKEN
        },function () {

    })
}

function search_UMLS() {
    var str = document.getElementById("input-disease").value;
    status = 0;
    $("#api-response").html("<p>searching...</p>");
    var tgt = session['tgt'];
    var st = "loop";
    if(tgt){
        get_st_from_UMLS(tgt);
        st = serviceTicket;
    } else {
        console.log("from Auth:");
        st = get_api_from_UMLS();
    }
    if(status != 200){
        return
    }
    url = "https://uts-ws.nlm.nih.gov/rest/search/current";
    $.getJSON(url, {"string":str,"ticket":st},load);
}

function load(res) {
    $("#api-response").html("");
    var results = res.result.results;
    var result_length = results.length>6?6:results.length;
    for (var l = 0; l<result_length; l++){
        $("#api-response").append("<p><b>"+ results[l].ui +"</b> - <b>"+ results[l].name +"</b></p>");
    }
}

function start(){
    var new_url = API_PATH + 'quiz/disease/1/';
    location.href = new_url;
}


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
        API_PATH + "umls-auth",
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
function after_add() {
    $(".selected-ans>.ans-btn").click(function () {
        $(".ans-list").append($(this));
    });
}

function next_question(){
    var $select_btns = $(".selected-ans button");
    var select_info = [];
    var type = "symptom";
    if($select_btns.length === 0){
        layer.msg("Please select correct symptoms or add new one.");
        return
    }
    for(var i = 0; i < $select_btns.length; i++){
        var ans = {};
        ans.id = $select_btns[i].id;
        ans.text = $($select_btns[i]).html();
        select_info[i] = ans;
    }
    var data = {};
    data["question_id"] = $(".question-head")[0].id.split("_")[1];
    data["selections"] = select_info;
    data["type"] = type;
    console.log(data);
    data = JSON.stringify(data);
    $.post(
        API_PATH + "upload-answer",
        {
            name:"answer",
            csrfmiddlewaretoken:CSRFTOKEN,
            data:data,
        },function (res) {
            res = JSON.parse(res);
            if(res.status == 20){
                layer.msg(res.result);
                setTimeout(1000,location.reload());

            }
        }
    )

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
        $("#api-response").append("<p><a id='" + results[l].ui +"' class='btn search-result'>"+ results[l].ui +" -  <b class='search-result-text'>"+ results[l].name +"</b>  - "+results[l].rootSource+"</a></p>");

    }
    searchResult();
}
function start(){
    var new_url = API_PATH + 'quiz/disease/'+ session.uuid +'/';
    location.href = new_url;
}

function searchResult() {
    $(".search-result").click(function () {
        var  text = $(this).children(".search-result-text").text();
        var  cui = $(this).attr("id");
        console.log(cui);
        $(".selected-ans").append("<button id='"+cui+"' class='btn btn-info mr-2 mb-2 ans-btn'>"+ text +"</button>");
        $(this).css("background-color","#fafafa");
    })
}
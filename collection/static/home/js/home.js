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
	    var res_list = res.result;
        // var result = res.result[0];
	    var def = "";
	    for(var i = 0; i < res_list.length; i++){
	    	if(res_list[i].rootSource == "MSH"){
	    		def = res_list[i].value;
		    }
	    }
	    if(def == ""){
	    	$("#disease-def").html("Sorry, there is no MSH defination about this disease.");
	    }else {
	    	$("#disease-def").html(def);
	    }
    }).fail(function () {
        $("#disease-def").html("Sorry, there is no defination about this disease.");
    });
}

function add_symptom(){
    var text = $("#input-disease").val();
    var $ans_list = $(".selected-ans .ans-btn");
    if($ans_list.length > 0) {
    	for ( var i=0; i < $ans_list.length; i++){
			console.log(text, " ? = ", $ans_list[i].innerText )
			if(text.toLowerCase() == $ans_list[i].innerText.toLowerCase()){
				layer.msg("Please select or input different term.");
			    return
			}
	    }
    };
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
        success:function (data) {
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

function next_question(obj){
    var type = session.type;
    var data = {};
    if(type.indexOf('valid')>0){
    	var ans = $(".valid-word").attr('id');
    	data["selections"] = parseInt(ans.split("_")[1]);
    	data["is_agree"] = $(obj).attr("value");
    }
    else{
	    var $select_btns = $(".selected-ans button");
	    var select_info = [];
	
	    if($select_btns.length === 0){
	        layer.msg("Please select correct answers or add new one.");
	        return
	    }
	    for(var i = 0; i < $select_btns.length; i++){
	        var ans = {};
	        ans.id = $select_btns[i].id;
	        ans.text = $($select_btns[i]).html();
	        select_info[i] = ans;
	    }
	    data["selections"] = select_info;
    }
    data["type"] = type;
    data["uuid"] = session.uuid;
    data["question_id"] = $(".question-head")[0].id.split("_")[1];
    console.log(data);
    data = JSON.stringify(data);

    $.post(
        API_PATH + "upload-answer",
        {
            name:"answer",
            csrfmiddlewaretoken:CSRFTOKEN,
            data:data
        },function (res) {
            res = JSON.parse(res);
            if(res.status == 20){
                layer.msg(res.result);
                setTimeout(1000,location.reload());
            } else if (res.status == 0){
                layer.msg(res.result);
            }
        }
    )
}

function search_database(type) {
	var str = document.getElementById("input-disease").value;
    status = 0;
    $("#api-response").html("<p>searching...</p>");
    if(str.length <= 1 || str == "" || str == " "){
    	if(str == "" || str == " ")$("#api-response").html("<p></p>");
	    return
    }
    else{
		var url =  API_PATH + "search-terms";
		$.getJSON(url, {"str":str,"type":type},load_searching);
    }

}

function load_searching(res) {
	if (res.status == 0){
		$("#api-response").html(res.results);
		return
	}
    $("#api-response").html("");
    var results = res.results;
    var result_length = results.length>6?6:results.length;
    for (var l = 0; l<result_length; l++){
        $("#api-response").append("<p><a id='" + results[l].id +"' class='btn search-result'>"+ results[l].cui +" -  <b class='search-result-text'>"+ results[l].name +"</b></a></p><p class='def'>"+ results[l].type +": " +results[l].def +"</p>");
    }
    searchResult();
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
        st = get_api_from_UMLS();
    }
    if(status != 200){
        return
    }
    url = "https://uts-ws.nlm.nih.gov/rest/search/current";
    $.getJSON(url, {"string":str,"ticket":st},load_UMLS_searching);
}

function load_UMLS_searching(res) {
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
        var $ans_list = $(".selected-ans .ans-btn");
        if($ans_list.length > 0) {
            for ( var i=0; i < $ans_list.length; i++){
                console.log(text, " ? = ", $ans_list[i].innerText )
                if(text.toLowerCase() == $ans_list[i].innerText.toLowerCase()){
                    layer.msg("Please select or input different term.");
                    return
                }
            }
        };
        $(".selected-ans").append("<button id='"+cui+"' class='btn btn-info mr-2 mb-2 ans-btn'>"+ text +"</button>");
        $(this).css("background-color","#fafafa");
    })
}

$(function () {

    $(".ans-list>.ans-btn").click(function () {
        $(".selected-ans").append($(this));
    });

    $('#input-disease').on('input',function(){
        search_UMLS();
    });


})


//for ie
if(document.all){
    $('input[type="text"]').each(function() {
        var that=this;

        if(this.attachEvent) {
            this.attachEvent('onpropertychange',function(e) {
                if(e.propertyName!='value') return;
                $(that).trigger('input');
            });
        }
    })

}
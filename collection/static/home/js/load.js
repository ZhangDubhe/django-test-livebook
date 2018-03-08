
$(function () {

    $(".ans-list>.ans-btn").click(function () {
        $(".selected-ans").append($(this));
    });

    $('#input-disease').on('input',function(){
        // search_database();
    });

    $(".agree-div button").click(function () {
        $('.agree').removeClass('btn-secondary').addClass('btn-outline-secondary');
        $('.agree').removeClass('active');
        $('.disagree').removeClass('btn-secondary').addClass('btn-outline-secondary');
        $('.disagree').removeClass('active');
        $(this).removeClass('btn-outline-secondary').addClass('btn-secondary');
        $(this).addClass('active');
    })
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
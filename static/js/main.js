
$(document).ready(function(){

    $('#contact_table').DataTable();

    $(document).on("click", "a[name='a_fav']", function(e){
        e.preventDefault();
        url = this.attributes.href.value;
        var self = $(this);
        $.ajax({
            type: "POST",
            url: url,
            data: {'csrfmiddlewaretoken': getCookie('csrftoken')},
            dataType: 'json',
            success: function(response){
                if(response.fav_value == true){
                    self.children().attr('class', 'fa fa-star');
                }
                else{
                    self.children().attr('class', 'fa fa-star-o');
                }
            }
        });
    });

    $(document).on("click", "a[name='a_remove']", function(e){

        e.preventDefault();
        url = this.attributes.href.value;
        var self = $(this);

        $.confirm({
            title: false,
            icon: 'fa fa-question-circle-o',
//            theme: 'supervan',
            closeIcon: true,
            animation: 'scale',
            type: 'red',
            buttons: {
                Delete: function () {
                    $.ajax({
                        type: "POST",
                        url: url,
                        data: {'csrfmiddlewaretoken': getCookie('csrftoken')},
                        dataType: 'json',
                        success: function(response){
                            self.parent().parent().remove();
                        }
                    });
                },
                Cancel: function () {
                },
            },
        });
    });

    $(document).on("click", "a[name='a_edit']", function(e){
//        e.preventDefault();
//        url = this.attributes.href.value;
//        var self = $(this);
        model = $("#modal_contact");
        model.show();
//        $.ajax({
//            type: "POST",
//            url: url,
//            data: {'csrfmiddlewaretoken': getCookie('csrftoken')},
//            dataType: 'json',
//            success: function(response){
//                model.modal();
//                $.each(response.data, function(id, val){
//                    el = model.find('#id_'+id);
//                    el.val(val)
//                });
//            }
//        });
    });



    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
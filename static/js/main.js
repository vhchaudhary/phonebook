
$(document).ready(function(){

    $('#contact_table').DataTable({
        "bPaginate": true,
        "bLengthChange": false,
        "bFilter": true,
        "bInfo": false,
        "bAutoWidth": true,
        'aoColumnDefs': [{
            'bSortable': false,
            'aTargets': [0]
            }]
    });

    div_btn_multi = $("#contact_table_wrapper").children().first().children().first();
    div_btn_multi.append("<button class='btn btn-danger btn-sm' id='btn_dlt_multi' hidden>Delete Selected</button>");

    select_all = $(".sorting_asc")
    select_all.first().html("<input type='checkbox' id='select-all-check'>")
    select_all.addClass("nosort").removeClass("sorting_asc")

    $(document).on("click", "#select-all-check", function(){
        if($(".selected").length == 0){
            $('.select-multiple').parent().parent().addClass('selected');
            $('.select-multiple').prop('checked', true);
            $("#btn_dlt_multi").attr("hidden",false);
        }
        else{
            $('.select-multiple').parent().parent().removeClass('selected');
            $('.select-multiple').prop('checked', false);
            $("#btn_dlt_multi").attr("hidden",true);
        }

    });

    $(document).on("click", ".select-multiple", function(){
        row = $(this).parent().parent();
        if(row.hasClass('selected')) {
            row.removeClass('selected');
            if($(".selected").length == 0){
                $("#btn_dlt_multi").attr("hidden",true);
            }
        }
        else {
            row.addClass('selected');
            $("#btn_dlt_multi").attr("hidden",false);
        }
    });

    $(document).on("submit", "#form_import_vcf", function(e){
        e.preventDefault();
        var form_data = new FormData(this);
        $.ajax({
            type: this.attributes.method.value,
            url: this.attributes.action.value,
            data: form_data,
            dataType: 'json',
            cache: false,
            processData: false,
            contentType: false,
            success: function(response){
                $("#modal_imp_contact").hide();
                alert(response.message);
            }
        });
    });

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

    $(document).on("click", "#btn_dlt_multi", function(e){
        e.preventDefault();
        var self = $(this);
        ids = [];
        selected = $(".select-multiple:checked")
        selected.each(function(){
            ids.push($(this).attr('data'));
        });
        $.confirm({
            title: false,
            icon: 'fa fa-question-circle-o',
            closeIcon: true,
            animation: 'scale',
            type: 'red',
            buttons: {
                Delete: function () {
                    $.ajax({
                        type: "POST",
                        url: "/delete_multi/",
                        data: {'csrfmiddlewaretoken': getCookie('csrftoken'), 'ids': ids},
                        dataType: 'json',
                        success: function(response){
                            if(response.success == true){
                                selected.parent().parent().remove();
                            }
                        }
                    });
                },
                Cancel: function () {
                },
            },
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
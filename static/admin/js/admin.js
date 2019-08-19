

(function($) {
    $(document).on("submit", "#contact_form", function(event){
        form_name = $(this).parents("form").first().attr('id')
        event.preventDefault();
        alertify.confirm("This is a confirm dialog.",
        function(){
            event.currentTarget.submit();
        }).set({title:"Update"});
    });
})(django.jQuery);
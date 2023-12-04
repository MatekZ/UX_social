$(document).ready(function () {
    $('#show_form').click(function () {
        $('.ui.modal').modal('show');
    })

    $('#show_post_form').click(function () {
        $('.coupled.modal').modal({
            allowMultiple: false
        });

        $('.second.modal').modal('attach events', '.first.modal .text-post');
        $('.third.modal').modal('attach events', '.first.modal .image-post');

        $('.first.modal').modal({
            transition: 'fade up'
        }).modal('show');
    })

    $('.ui.dropdown').dropdown()
})
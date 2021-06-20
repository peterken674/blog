$(document).ready( function () {
    $('[data-toggle="popover"]').popover({
        html: true,
        trigger: 'click',
        content: function () {
            return $('#popover-content').html();
        }
    });
});
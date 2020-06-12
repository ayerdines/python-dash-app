$(function () {
    $(document).on('click', '#sidebarCollapse', function (event) {
        event.preventDefault();
        $("#wrapper").toggleClass("toggled");
    });
});
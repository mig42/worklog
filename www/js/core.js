$(document).ready(function () {
    fadeScrollToTop();
    fadeScrollToBottom();

    $(window).scroll(function () {
        fadeScrollToTop();
        fadeScrollToBottom();
    });
    $('.totop').click(function () {
        $("html, body").animate({
            scrollTop: 0
        }, 600);
        return false;
    });
    $('.tobottom').click(function () {
        $("html, body").animate({
            scrollTop: $(document).height()
        }, 600);
        return false;
    });
});

function fadeScrollToTop() {
    if ($(window).scrollTop() > 100) {
        $('.totop').fadeIn();
        return;
    }
    $('.totop').fadeOut();
}

function fadeScrollToBottom() {
    if ($(window).scrollTop() + $(window).height() > $(document).height() - 100) {
        $('.tobottom').fadeOut();
        return;
    }
    $('.tobottom').fadeIn();
}
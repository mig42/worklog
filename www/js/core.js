$(document).ready(function () {
    fadeScrollTop();
    fadeScrollBottom();

    $(window).scroll(function () {
        fadeScrollTop();
        fadeScrollBottom();
    });
    $('.scrolltop').click(function () {
        $("html, body").animate({
            scrollTop: 0
        }, 600);
        return false;
    });
    $('.scrollbottom').click(function () {
        $("html, body").animate({
            scrollTop: $(document).height()
        }, 600);
        return false;
    });
});

function fadeScrollTop() {
    if ($(window).scrollTop() > 100) {
        $('.scrolltop').fadeIn();
        return;
    }
    $('.scrolltop').fadeOut();
}

function fadeScrollBottom() {
    if ($(window).scrollTop() + $(window).height() > $(document).height() - 100) {
        $('.scrollbottom').fadeOut();
        return;
    }
    $('.scrollbottom').fadeIn();
}
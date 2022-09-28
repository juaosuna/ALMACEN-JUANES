'use strict';

(function ($) {
    if ($(window).outerWidth() > 992) {
        $(".custom-scrollbar").mCustomScrollbar({
            scrollInertia: 200,
            theme:"dark-thin"
        });
    }
}(jQuery));
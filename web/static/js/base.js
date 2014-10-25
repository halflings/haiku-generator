// error notification zone
var errorMessage = function(msg) {
    error_bar.text(msg);
    error_bar.slideDown(300).delay(3000).slideUp(300);
};

$(document).ready(function() {
    error_bar = $('#error-bar');

    // document.ready code should go here
});
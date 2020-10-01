var AnimEnd = 'animationend webkitAnimationEnd mozAnimationEnd MSAnimationEnd oAnimationEnd';
var nav = $('.nav');
var navButton = $('.nav-el');
var overlay = $('.overlay');

$(navButton).click(function(event){

    if ($(this).hasClass("inactive")) {
        event.preventDefault();

    } else {

        // 移除previous
        $(navButton).removeClass('inactive_reverse active_reverse');
        $(nav).removeClass('fx-box_rotate fx-box_rotate_reverse');
        $(overlay).removeClass('active active_reverse');

        /* Add classes on defined elements */
        $(this).siblings().addClass('inactive');
        $(this).addClass('active');
        $(nav).addClass('fx-box_rotate');

        var o_target = $(this).data('id');
        $('#'+o_target).addClass('active');

        $("body").addClass('noscroll');

    }

});

//关闭
$(".close").click(function(){

    //添加跳转样式
    $('.active', nav).removeClass('active').addClass('active_reverse');
    $('.inactive', nav).addClass('inactive_reverse');
    $(nav).addClass('fx-box_rotate_reverse');
    $(this).parent().addClass('active_reverse');

    /* Remove .noscroll and .inactive when animation is finished */
    $('.inactive_reverse').bind(AnimEnd, function(){

        $('body').removeClass('noscroll');
        $(navButton).removeClass('inactive');
        $('.inactive_reverse').unbind(AnimEnd);

    });

});
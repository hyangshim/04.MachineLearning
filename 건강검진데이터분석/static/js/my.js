$(function () {
    $(".left_sub_menu1").hide();
    $(".has_sub1").click(function () {
        $(".left_sub_menu1").fadeToggle(300);
    });
    // 왼쪽메뉴 드롭다운
    $(".sub_menu1 ul.small_menu").hide();
    $(".sub_menu1 ul.big_menu").click(function () {
        $("ul", this).slideToggle(300);
    });
    $(".left_sub_menu2").hide();
    $(".has_sub2").click(function () {
        $(".left_sub_menu2").fadeToggle(300);
    });
    $(".sub_menu2 ul.big_menu").click(function () {
        $("ul", this).slideToggle(300);
    });
    // 외부 클릭 시 좌측 사이드 메뉴 숨기기
    $('.overlay').on('click', function () {
        $('.left_sub_menu1').fadeOut();
        $('.left_sub_menu2').fadeOut();
        $('.hide_sidemenu').fadeIn();
    });
});

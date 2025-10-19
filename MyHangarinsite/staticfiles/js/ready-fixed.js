$(function() {
  $('[data-toggle="tooltip"]').tooltip();
});

jQuery(document).ready(function() {
  // Removed jQuery(".scrollbar-inner").scrollbar();
});

$(document).ready(function() {
  var t = false, o = false, e = 0, a = 0;

  if (!t) {
    $toggle = $(".sidenav-toggler");
    $toggle.click(function() {
      if (e == 1) {
        $("html").removeClass("nav_open");
        $toggle.removeClass("toggled");
        e = 0;
      } else {
        $("html").addClass("nav_open");
        $toggle.addClass("toggled");
        e = 1;
      }
    });
    t = true;
  }

  if (!o) {
    $topbar = $(".topbar-toggler");
    $topbar.click(function() {
      if (a == 1) {
        $("html").removeClass("topbar_open");
        $topbar.removeClass("toggled");
        a = 0;
      } else {
        $("html").addClass("topbar_open");
        $topbar.addClass("toggled");
        a = 1;
      }
    });
    o = true;
  }

  $('[data-select="checkbox"]').change(function() {
    $target = $(this).attr("data-target");
    $($target).prop("checked", $(this).prop("checked"));
  });
});

$(document).ready(function(){
  $('.button-collapse').sideNav();
  $('select').material_select();
  $(".dropdown-button").dropdown({
    belowOrigin: true, // Displays dropdown below the button
    hover: true, // Activate on hover
  });
  $('.modal-trigger').leanModal(); // Open a mini window in the same page 
});

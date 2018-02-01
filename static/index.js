$( ".go-button" ).click(function() {

  value = $('.search-text').val()

  if (value.length == 0) {
    return
  }

  $('.search tbody tr').remove();

  $(".search").css("visibility", "visible");

  data = {"word" : value}
  $.post("/search",data,
    function(data, status) {
      for (var i = 0; i < data.length; i++) {
          $('.search tbody').append("<tr><td>" + data[i].code + "</td><td>" + data[i].name + "</td><td>" + data[i].open + "</td><td>" + data[i].high + "</td><td>" + data[i].low + "</td><td>" + data[i].close + "</td></tr>");
      }
    }
  ,dataType = "json");

});

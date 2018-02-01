$(document).ready(function() {
  var top_table = $('#top_stocks').DataTable({
      "searching": false
      });

   var search_table = $('#search').DataTable({
      "searching": false,
      });

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
          search_table.row.add( [
            data[i].code,
            data[i].name,
            data[i].open,
            data[i].high,
            data[i].low,
            data[i].close
        ] ).draw( false );
      }
    }
  ,dataType = "json");

});

} );

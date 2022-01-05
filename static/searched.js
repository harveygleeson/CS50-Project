
var table = document.getElementById("tableID");

for (var i = 1; i < table.rows.length; i++) {

  table.rows.item(i).onclick = function () {
    var table_cells = this.cells;

    var song_id = table_cells.item(4).innerHTML;
    $.post("/hosting/$(location)", {
      "song_id":song_id
      // "sender_id": {{ sender_id }}
    });
  }
}

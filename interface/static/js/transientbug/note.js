$(function() {
  $("#del_btn").click(function() {
    var yesno = confirm("Are you sure you want to delete this note?");

    if(yesno) {
      var img=$(this).data("short");

      $.post("/notes/edit/"+img+"/delete", function(data) {
        if(data[0]["success"]) {
          window.location.href="/notes";
        }
      });
    };
  });

  var editor = new EpicEditor({
    theme: {
      base: 'css/lib/epic/base/epiceditor.css',
      preview: 'css/lib/epic/preview/github.css',
      editor: 'css/lib/epic/editor/epic-dark.css'
    },
    basePath: '/static/',
    autogrow: {
      minHeight: 200
    },
    textarea: "content"
  }).load();

  editor.on('update', function () {
    $("#preview").html(this.exportFile(null, 'html'));
  }).emit('update');

  $("#tags").pillbox();

  var tags = $.ajax({url: "/notes/tags/json", async: false});

  $('.pillbox input').typeahead({
    name: 'notes_tags',
    local: tags.responseJSON[0],
    limit: 10
  });
});

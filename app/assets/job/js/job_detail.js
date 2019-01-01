$(function() {
    var converter = new showdown.Converter({
      simplifiedAutoLink: true
    });

    description_html = converter.makeHtml($("#job_description").text());
    $("#job_description").replaceWith(description_html);
    $("#job_description").show();
});

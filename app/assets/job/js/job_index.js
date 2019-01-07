$('input[type="radio"]').on('click change', function(e) {
  $('#job-filter').submit();
});
$('input[type="checkbox"]').on('click change', function(e) {
  $('#job-filter').submit();
});

function addTag(tag) {
  $('.filter-tags').append('<a class="filter-tag keywords"><span>' + value + '</span>' +
    '<i class="fas fa-times" onclick="removeFilter(\'keywords\', \'' + value + '\')"></i></a>');
};

$('#search').on('keydown', function(event) {
if (event.keyCode === $.ui.keyCode.ENTER) {
    event.preventDefault();
    $('#job-filter').submit();
  }
});

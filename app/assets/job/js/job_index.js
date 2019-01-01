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

$('#search').on('input', function() {
  if ($(this).val()) {
    $('.close-icon').show();
  } else {
    $('.close-icon').hide();
  }
})
// don't navigate away from the field on tab when selecting an item
.on('keydown', function(event) {
  if (event.keyCode === $.ui.keyCode.TAB && $(this).autocomplete('instance').menu.active) {
    event.preventDefault();
  } else if (event.keyCode === $.ui.keyCode.ENTER) {
    event.preventDefault();
    $('#job-filter').submit();
  }
})
.autocomplete({
  minLength: 0,
  source: function(request, response) {
    // delegate back to autocomplete, but extract the last term
    // response($.ui.autocomplete.filter(document.keywords, extractLast(request.term)));
  },
  focus: function() {
    // prevent value inserted on focus
    return false;
  },
  select: function(event, ui) {
    var terms = split(this.value);

    $('.close-icon').hide();

    // remove the current input
    terms.pop();

    // add the selected item
    terms.push(ui.item.value);

    // add placeholder to get the comma-and-space at the end
    terms.push('');

    this.value = '';

    addTag(ui.item.value);

    return false;
  }
});

function onSelectedTextReceived(selectedTextInfo) {
  document.getElementById('status').style.display = 'none';
  document.getElementById('hd_title').value = selectedTextInfo.title;
  document.getElementById('hd_url').value = selectedTextInfo.url;
  document.getElementById('excerpt').innerHTML = selectedTextInfo.text;
}

window.addEventListener('load', function(e) {
  
  var console = chrome.extension.getBackgroundPage().console;

  chrome.runtime.getBackgroundPage(function(eventPage) {
    eventPage.getSelectedTextData(onSelectedTextReceived);
  });

  $('#save_data').click( function() {
    post_data = {
          about: $('#key').val(),
          excerpt: $('#excerpt').text(),
          url: $('#hd_url').val(),
          title: $('#hd_title').val()
        };
    console.log(post_data);
    $.post(
      'http://localhost:5000/save', 
      post_data,
      function(data, status) {
        $('#status').show() ;
        $('#data_form').hide() ;
        $('#status').html('<h3>Ok, saved!</h3>');
      });
  });

});

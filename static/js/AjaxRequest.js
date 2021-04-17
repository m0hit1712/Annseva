
function send_ajax(dict, callback) {
  url = dict["url"] 
  data = dict["data"]
  $.ajax({
    url: url,
    data: data,
    async: true,
    dataType: "json",
    success: function (data) {
      callback(data)
    },
  });
}




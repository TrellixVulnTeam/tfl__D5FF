var endpoint = '/api/dashboard/';
$.ajax({
    method: "GET",
    url: endpoint,

    success: function (data) {
        console.log(data);
    },
    error: function (error_data) {
        console.log("error");
        console.log(error_data);
    }
});




//Change function for validate quantity
function validate_quantity(product_id, product_quantity) {
      $.ajax({
            url: 'validate_quantity/',
            type: 'POST',
            data: {
                  'product_id': product_id,
                  'product_quantity': product_quantity
            },
            dataType: 'json',
            success: function (data) {
                  if (true) {
                        alert("A user with this username already exists."+data.test);
                  }
            }
      });
}
//Change function for validate quantity
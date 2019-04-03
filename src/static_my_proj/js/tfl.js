//Function for validate quantity
function validate_quantity(product_id, product_quantity) {
      $.ajax({
            type: 'POST',
            url: 'validate_quantity/',
            data: {
                  'product_id': product_id,
                  'product_quantity': product_quantity
            },
            dataType: 'json',
            success: function (data) {
                  if (data) {
                        document.getElementById('total_weight').innerHTML ="Weight: " + data.total_weight;
                        document.getElementById('total_price').innerHTML ="Total: " + data.total_price;
                  }
            }
      });
}
//Function for validate quantity

//For cart field
function cart_field_change(field_name, field_value, date_field) {
      //console.log(clean_func);
      $.ajax({
            type: 'POST',
            url: 'cart_field_change/',
            data: {
                  'field_name': field_name,
                  'field_value': field_value,
                  'date_field': date_field
            },
            dataType: 'json',
            success: function (data) {
                  if (data) {
                        alert("Value: " + data.field_value + " " + date_field);
                  }
            }
      });
}

function cart_product_remove(product_id) {
      //console.log(cart_id+"-"+product_id);
      $.ajax({
            type: 'POST',
            url: 'remove/',
            data: {
                  'product_id': product_id
            },
            dataType: 'json',
            success: function (data) {
                  if (data) {
                        window.location.reload();
                  }
            }
      });
}
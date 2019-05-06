function add_to_cart(product_id) {
      $.ajax({
            type: 'POST',
            url: 'cart/add/',
            data: {
                  'product_id': product_id
            },
            dataType: 'json',
            success: function (data) {
                  if (data.refresh === 'true') {
                        document.getElementById('cart_count').innerHTML = data.cart_count;
                  }
            }
      });
}

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
                  console.log(data);
                  if (data['error'] === 'true') {
                        alert(data['error_message'])
                  }
            }
      });
}


function set_company(company_id){
      $.ajax({
            type: 'POST',
            url: 'set_company/',
            data: {
                  'company_id': company_id
            },
            dataType: 'json',
            success: function (data) {

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

function confirm_order(order_id) {
      //console.log("Order: "+order_id);

      $.ajax({
            type: 'POST',
            url: 'confirm/',
            data: {
                  'order_id': order_id
            },
            dataType: 'json',
            success: function (data) {
                  if (data) {
                        window.location.reload();
                  }
            }
      });
}

function order_edit(cart_id) {
      //console.log("Order: "+order_id);

      $.ajax({
            type: 'POST',
            url: 'edit_order/',
            /*data: {
                  'cart_id': cart_id
            },
            dataType: 'json',*/
            success: function (data) {
                  if (data['refresh'] === 'true') {
                        window.location.href = 'http://localhost:8000/cart/';
                  }
            }
      });
}


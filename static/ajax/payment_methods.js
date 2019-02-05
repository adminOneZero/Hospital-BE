$( document ).ready(function() {


  /**************************flash system************************/
  iziToast.settings({
      timeout: 9000,
      layout: 2,
      rtl: true,
      titleColor: '#fff',
      iconColor: '#fff',
      progressBarColor: '#fff',
      messageColor: '#fff',
      titleColor: '#fff',
      class : 'notify',
      resetOnHover: true,
      icon: 'material-icons',
      transitionIn: 'flipInX',
      transitionOut: 'flipOutX',
      position: 'topLeft', // bottomRight, bottomLeft, topRight, topLeft, topCenter, bottomCenter, center
  });


  function flash(message,type = 'default') {
    // normal flash
    if (type == 'default' || type == '' || type == 'undefined') {
      iziToast.show({
        iconText: '✿',
        message: message,
        backgroundColor: 'rgb(114,54,139,0.7)',
      });
    }

    // danger flash
    if (type == 'danger') {
      iziToast.show({
        title: ' خطأ ',
        iconText: '✘',
        message: message,
        backgroundColor: 'rgb(192,57,43,0.7)',
      });
    }

    // success flash
    if (type == 'success') {
      iziToast.show({
        title: ' نجاح ',
        iconText: '😍',
        message: message,
        backgroundColor: 'rgb(30 ,100,72,0.7)',
      });
    }

    // warning flash
    if (type == 'warning') {
      iziToast.show({
        title: ' تنبيه ',
        iconText: '🚧',
        message: message,
        backgroundColor: 'rgb(243 ,156  ,18,0.8)',
      });
    }


  }

  /**************************global flash************************/

  $.get("/flash" ,function(data, status){

    if (status == 'success') {
      if (data.length > 0 ) {
        $.each(data, function(key, value){
            flash(value,'warning');
            });
      }


    }

  });



  /**************************payment methods************************/

  // saving new clinic data
  $('#save_btn').on('click',function(){

    if (this.dataset.action == 'add') {

      var payment         =  $('form input[name=payment]:checked').val();
      var discount_type   =  $('input[name=discount]:checked').val();
      var discount_value  =  $('input[name=percentage_input]').val();
      var ar_name         =  $('form input[name=ar_name]').val();
      var en_name         =  $('form input[name=en_name]').val();
      var Go = true;


      // currect errors
      if ( typeof payment == 'undefined') {
        flash(' يجب اختيار طريقه الدفع ','danger');
        Go = false
      }
      // show warning if user donot use discounting
      if (typeof discount_type == 'undefined' || discount_value == '' ) {

        flash(' لاتوجد اي نسبه خصم ','warning');
        var discount  = 0 ;

      }else{ // if no problem

        if (discount_type == 'percentage') {

          var discount_value  =  $('input[name=percentage_input]').val();

          if (discount_value == '') {
            var discount_value  = 0 ;
            Go = false
          }

        }else if (discount_type == 'static') {

          var discount_value =  $('input[name=static_input]').val();

          if (discount_value == '') {
            var discount_value  = 0 ;
            Go = false
          }
        }
      }
      if (en_name == '') {
        flash(' ادخل اسم الشركه بالانجليزيه ','danger');
        Go = false
      }

      if (ar_name == '') {
        flash(' ادخل اسم الشركه بالعربي ','danger');
        Go = false
      }

      if (Go) {

      // add new clinics
      $.post("/api/payment_methods/add", { payment: payment , discount_value : discount_value , ar_name: ar_name, en_name: en_name , discount_type : discount_type},
      function(data, status){
        if (typeof(data) == 'object' && status == 'success') {
          if ('message' in data) {
            flash(data['message'],data['MSG_type']);
            // reset inputs to null
            if (data['MSG_type'] == 'success') {
              $('form input').val('');
            }

          }

        }

      });
    }

    }



  });





});

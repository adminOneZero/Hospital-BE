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
      var discount_value  =  '';
      var ar_name         =  $('form input[name=ar_name]').val();
      var en_name         =  $('form input[name=en_name]').val();
      var Go = true;

      // if the type of discount is percentage get the value of percentage input
      if (discount_type == 'percentage') {
        discount_value  =  $('input[name=percentage_input]').val();
      }else{
        discount_value  =  $('input[name=static_input]').val();
      }
      // currect errors
      if ( typeof payment == 'undefined') {
        flash(' يجب اختيار طريقه الدفع ','danger');
        Go = false
      }
      // show warning if user donot use discounting
      if (typeof discount_type == 'undefined' || discount_value == '' ) {

        flash(' لاتوجد اي نسبه خصم ','warning');
        var discount_value  = 0 ;

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


  // deleting a services data
  $(document).on('click','.delete',function(event){
    event.preventDefault();

    var db_id = this.dataset.delete_id

    $.post("/api/payment_methods/delete", { db_id: db_id },
    function(data, status){
      if (typeof(data) == 'object' && status == 'success') {

      flash(data['message'],data['MSG_type']);
      if (data['MSG_type'] == 'success') {
        window.setTimeout(function(){
          // reload page
          location.reload();

        }, 4000);

      }


      }
    });


  });



  /*************** editing payment methods dataset ***************/

  // editing a payment methods data
  $(document).on('click','.edit',function(event){
    event.preventDefault();
    $('#save_btn').attr('data-action','update');

    var db_id = this.dataset.edit_id;


    $.post("/api/payment_methods/edit", { db_id: db_id },
    function(data, status){
      if (typeof(data) == 'object' && status == 'success') {

        var db_id            = data['db_id'];
        var ar_name          = data['ar_name'];
        var en_name          = data['en_name'];
        var method           = data['method'];
        var discount_type    = data['discount_type'];
        var discount_value   = data['discount_value'];

        $('form input[name=db_id]').val(db_id);
        $('form input[name=ar_name]').val(ar_name);
        $('form input[name=en_name]').val(en_name);
        $('form input[value='+method+']').attr('checked', 'checked');
        if (discount_type == 'percentage') {
          $('form input[value='+discount_type+']').attr('checked', 'checked');
          $('form input[name=percentage_input]').val(discount_value);

        }else{
          $('form input[value='+discount_type+']').attr('checked', 'checked');
          $('form input[name=static_input]').val(discount_value);
        }

        $('.mod').iziModal('open',{zindex: 4 });


      }
    });


  });



  // save updateing data
  $(document).on('click','#save_btn',function(){
    // check current action
  if (this.dataset.action == 'update') {

    var service_code = $('form input[name=service_code]').val();
    var service_id   = $('form input[name=db_id]').val();
    var ar_name      = $('form input[name=ar_name]').val();
    var en_name      = $('form input[name=en_name]').val();
    var service_cost = $('form input[name=service_cost]').val();
    var clinic = $('form select').val()
    console.log(service_cost);
    $.post("/api/services/update", { service_code: service_code , service_id : service_id, en_name : en_name , ar_name : ar_name ,service_cost:service_cost,clinic:clinic},
    function(data, status){
      if (typeof(data) == 'object' && status == 'success') {
        if ('message' in data) {
          flash(data['message'],data['MSG_type']);


        }

      }

    });

  }

  });




  // deleting a services data
  $(document).on('click','.delete',function(event){
    event.preventDefault();

    var db_id = this.dataset.delete_id

    $.post("/api/services/delete", { db_id: db_id },
    function(data, status){
      console.log(data);
      if (typeof(data) == 'object' && status == 'success') {

      flash(data['message'],data['MSG_type']);
      if (data['MSG_type'] == 'success') {
        window.setTimeout(function(){
          // reload page
          location.reload();

        }, 4000);

      }


      }
    });


  });





  // save updateing data
  $(document).on('click','#save_btn',function(){
    // check current action
  if (this.dataset.action == 'update') {
console.log(this.dataset.action);
    var payment         =  $('form input[name=payment]:checked').val();
    var discount_type   =  $('input[name=discount]:checked').val();
    var discount_value  =  '';
    var ar_name         =  $('form input[name=ar_name]').val();
    var en_name         =  $('form input[name=en_name]').val();
    var db_id           =  $('form input[name=db_id]').val();
// console.log(db_id);

    if (discount_type == 'percentage') {
      discount_value  =  $('input[name=percentage_input]').val();
    }else{
      discount_value  =  $('input[name=static_input]').val();
    }

    // console.log(service_cost);
    $.post("/api/payment_methods/update", { payment:payment ,  discount_type:discount_type ,  discount_value:discount_value ,  ar_name:ar_name ,  en_name:en_name ,db_id:db_id  },
    function(data, status){
      if (typeof(data) == 'object' && status == 'success') {
        if ('message' in data) {
          flash(data['message'],data['MSG_type']);

        }

      }

    });

  }

  });



  // SEARCH data
  $(document).on('click','#search',function(event){
    event.preventDefault();
    console.log('yes');
    var search = $('#search_box').val();
    $.post("/api/payment_methods/search", { search : search },
    function(data_search, status){

      // message
    if (typeof(data_search) == 'object' && status == 'success') {
      if (data_search['message']) {
        flash(data_search['message'],data_search['MSG_type']);
      }

      // show result of search
  if (!data_search['message'] &&  typeof data_search[0] != 'undefined' ) {
    $( '#search_table' ).html('') // reset search table
    $.each( data_search , function( index , row ) {

              // check
              var mark = '';
              var discount_type = '';
              if (row['discount_type'] == 'monetary') {
                mark = '$';
                discount_value = ' نقدي ';
              }else {
                mark = '%';
                discount_value = ' آجل ';
              }


             $( '#search_table' ).append(`

                    <tr>
                        <td>`+index+`</td>
                        <td>`+row['ar_name']+`</td>
                        <td>`+row['en_name']+`</td>
                        <td>`+discount_value+`</td>
                        <td>`+row['discount_value']+`<strong>`+mark+`</strong></td>
                        <td title="Edit"><a data-edit_id="`+row['db_id']+`" href="#" class="far fa-edit move-rotate edit"></a></td>
                        <td title="Delete"><a data-delete_id="`+row['db_id']+`" href="#" class="fas fa-trash move-rotate delete"></a></td>
                    </tr>

               `);
            console.log(index);
         });

    $('#search_result').iziModal('open',{zindex: 3 });

  }
      }
    });


  });



});

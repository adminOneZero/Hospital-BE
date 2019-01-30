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




/**************************Services************************/

// saving new clinic data
$('#save_btn').on('click',function(){



  if (this.dataset.action == 'add') {
    console.log(this.dataset.action);
    var service_code  =  $('form input[name=service_code]').val();
    var ar_name       =  $('form input[name=ar_name]').val();
    var en_name       =  $('form input[name=en_name]').val();
    var service_cost  =  $('form input[name=service_cost]').val();
    var inner_clinic  =  $('select[name=inner_clinic]').val();


    // add new service
    $.post("/api/services/add", {service_code : service_code,ar_name : ar_name,en_name : en_name,service_cost : service_cost,inner_clinic : inner_clinic},
    function(data, status){
      if (typeof(data) == 'object' && status == 'success') {
        if ('message' in data) {
          flash(data['message'],data['MSG_type']);
          // if request success reset all inputs to null
          if (data['MSG_type'] == 'success') {
          // reset all inputs
            $('form input').val('');

          }

        }

      }

    });

  }



});


/*************** editing Services dataset ***************/

// editing a clinic data
$(document).on('click','.edit',function(event){
  event.preventDefault();
  $('#save_btn').attr('data-action','update')

  var service_id = this.dataset.edit_id

  $.post("/api/services/edit", { service_id: service_id },
  function(data, status){
    if (typeof(data) == 'object' && status == 'success') {

      var service_id       = data['service_id']
      var service_code     = data['service_code']
      var ar_name          = data['ar_name']
      var en_name          = data['en_name']
      var clinic           = data['clinic']
      var service_costing  = data['service_costing']

      $('form input[name=service_code]').val(service_code);
      $('form input[name=db_id]').val(service_id);
      $('form input[name=ar_name]').val(ar_name);
      $('form input[name=en_name]').val(en_name);
      $('form input[name=service_cost]').val(service_costing);
      $('form select').html('');
      $.each(clinic, function( index, value ) {
        // alert( index + ": " + value );
        $('form select').append(`<option >`+value+`</option>`);
      });


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





// SEARCH data
$(document).on('click','#search',function(event){
  event.preventDefault();
  var search = $('#search_box').val();
  console.log('yes');
  $.post("/api/services/search", { search: search },
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
    //  index = index+1;
           $( '#search_table' ).append(`


<tr>
      <td> `+index+` </td>
      <td> `+row['service_code']+` </td>
      <td> `+row['ar_name']+` </td>
      <td>`+row['en_name']+`</td>
      <td> `+row['clinic']+` </td>
      <td> `+row['service_costing']+` </td>
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

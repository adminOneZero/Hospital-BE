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



/**************************clinics************************/

// saving new clinic data
$('#save_btn').on('click',function(){

  if (this.dataset.action == 'add') {
    console.log(this.dataset.action);

    var clinic_id =  $('form input[name=clinic_id]').val();
    var ar_name   =  $('form input[name=ar_name]').val();
    var en_name   =  $('form input[name=en_name]').val();

    // add new clinics
    $.post("/api/clinics/add", { clinic_id: clinic_id , ar_name: ar_name, en_name: en_name },
    function(data, status){
      if (typeof(data) == 'object' && status == 'success') {
        if ('message' in data) {
          flash(data['message'],data['MSG_type']);
          // reset inputs to null
          if (data['MSG_type'] == 'success') {
            $('form input[name=clinic_id]').val('');
            $('form input[name=ar_name]').val('');
            $('form input[name=en_name]').val('');
          }

        }

      }

    });

  }



});

/*************** editing clinics dataset ***************/

// editing a clinic data
$('.edit').on('click',function(event){
  event.preventDefault();
  $('#save_btn').attr('data-action','update')

  var clinic_id = this.dataset.edit_id

  $.post("/api/clinics/edit", { clinic_id: clinic_id },
  function(data, status){
    if (typeof(data) == 'object' && status == 'success') {
      var db_id     = data['id']
      var clinic_id = data['clinic_id']
      var ar_name   = data['ar_name']
      var en_name   = data['en_name']

      $('form input[name=db_id]').val(db_id);
      $('form input[name=clinic_id]').val(clinic_id);
      $('form input[name=ar_name]').val(ar_name);
      $('form input[name=en_name]').val(en_name);
      $('.mod').iziModal('open');


    }
  });


});


// updateing data
$('#save_btn').on('click',function(){
if (this.dataset.action == 'update') {
  console.log(this.dataset.action);
  var db_id =  $('form input[name=db_id]').val();
  console.log(db_id);
  var clinic_id =  $('form input[name=clinic_id]').val();
  var ar_name   =  $('form input[name=ar_name]').val();
  var en_name   =  $('form input[name=en_name]').val();

  $.post("/api/clinics/update", { clinic_id: clinic_id , ar_name : ar_name, en_name : en_name , db_id : db_id},
  function(data, status){
    if (typeof(data) == 'object' && status == 'success') {
      if ('message' in data) {
        flash(data['message'],data['MSG_type']);


      }

    }

  });

}

});



// deleting a clinic data
$('.delete').on('click',function(event){
  event.preventDefault();

  var db_id = this.dataset.delete_id

  $.post("/api/clinics/delete", { db_id: db_id },
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

});

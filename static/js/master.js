$(document).ready(function(){

if ($('.mod').attr('data-page-name') == 'doctors') {
  $("#page").iziModal({
    title: ' اضافه طبيب ',
    subtitle: ' اضافه اطباء جدد ',
    headerColor: 'rgb(0,0,10,0.7)',
    background: 'rgb(30,50,70,0.8)',
    transitionOutOverlay: 'fadeOut',
    loop: false,
    radius: 3,
    borderBottom: true,
  });

  // dataTables
  $('#tb').DataTable();
}

if ($('.mod').attr('data-page-name') == 'clinics') {
  $("#page").iziModal({
    title: ' اضافه عيادة  ',
    subtitle: ' اضف عيادة جديده ',
    headerColor: 'rgb(0,0,10,0.7)',
    background: 'rgb(30,50,70,0.8)',
    transitionOutOverlay: 'fadeOut',
    background: '#34495e',
    loop: false,
    zindex:1,
    radius: 3,
    borderBottom: true,
  });
}

if ($('.mod').attr('data-page-name') == 'medicine_service') {
  $("#page").iziModal({
    title: ' الخدمات الطبيه ',
    subtitle: ' اضافه خدمه جديده ',
    headerColor: 'rgb(0,0,10,0.7)',
    background: 'rgb(30,50,70,0.8)',
    transitionOutOverlay: 'fadeOut',
    background: '#34495e',
    loop: false,
    borderBottom: true,
  });
}
if ($('.mod').attr('data-page-name') == 'rooms') {
  $("#page").iziModal({
    title: ' الغرف ',
    subtitle: ' تصنيف الغرف ',
    headerColor: 'rgb(0,0,10,0.7)',
    background: 'rgb(30,50,70,0.8)',
    transitionOutOverlay: 'fadeOut',
    background: '#34495e',
    loop: false,
    radius: 3,
    borderBottom: true,
  });
}

if ($('.mod').attr('data-page-name') == 'payment_methods') {
  $("#page").iziModal({
    title: ' طرق الدفع ',
    subtitle: ' اضف طريقه دفع جديده ',
    headerColor: 'rgb(0,0,10,0.7)',
    background: 'rgb(30,50,70,0.8)',
    transitionOutOverlay: 'fadeOut',
    background: '#34495e',
    loop: false,
    radius: 3,
    borderBottom: true,
  });
}

if ($('.mod').attr('data-page-name') == 'users') {
  $("#page").iziModal({
    title: ' حسابات المستخدمين ',
    subtitle: ' اضف مستخدم جديد ',
    // fullscreen: true,
    openFullscreen: true,
    headerColor: 'rgb(0,0,10,0.7)',
    background: 'rgb(30,50,70,0.8)',
    transitionOutOverlay: 'fadeOut',
    background: '#34495e',
    loop: false,
    radius: 3,
    borderBottom: true,
  });
}


// modaliz search results
$("#search_result").iziModal({
  title: ' البحث ',
  subtitle: ' نتائج البحث ',
  headerColor: 'rgb(0,0,10,0.7)',
  background: 'rgb(30,50,70,0.8)',
  transitionOutOverlay: 'fadeOut',
  loop: false,
  width: '70%',
  padding:'10px 50px 10px 50px',
  radius: 3,
  borderBottom: true,
});


// on all page when click on add icon check the current page name
// and open its right modal
$(document).on('click', '.adding', function (event) {
  event.preventDefault();
  // reset inputs value before open
  $('#save_btn').attr('data-action','add')
  $('form input').val('');
  $('form input').val('');
  $('form input').val('');

// check current page name
  if (this.dataset.modal == 'doctors') {

    $('.mod').iziModal('open');

  }
  if (this.dataset.modal == 'clinics') {

    $('.mod').iziModal('open');

  }
  if (this.dataset.modal == 'medicine_service') {

    $('.mod').iziModal('open');

  }
  if (this.dataset.modal == 'payment_methods') {

    $('.mod').iziModal('open');

  }
  if (this.dataset.modal == 'users') {

    $('.mod').iziModal('open');

  }

});




// reload page btn
$('#reload_page').on('click',function(){
   location.reload();
});






});

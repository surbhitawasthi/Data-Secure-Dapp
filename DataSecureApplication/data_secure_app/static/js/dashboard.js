$(document).ready(function() {
    setTimeout(function() {
        $('#alert_message').fadeOut('fast');
    }, 2500);

    // Change the name of the uploaded file in the label name
    document.getElementById("inputGroupFile01").addEventListener('change',function(e){
        document.getElementById('fileName').innerHTML = document.getElementById("inputGroupFile01").files[0].name
    })
});
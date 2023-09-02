$(document).ready(function() {

  $('#registerForm').submit(function(event) {
      event.preventDefault(); // Prevent form submission

      var formData = new FormData(); // Create a FormData object

      // Append the form fields to the FormData object
      formData.append('name', $('#name').val());
      formData.append('email', $('#email').val());
      formData.append('otp', $('#otp').val());
      formData.append('password', $('#password').val());

      $.ajax({
          url: '/register/',
          method: 'POST',
          data: formData,
          contentType: false, // Prevent jQuery from setting content type
          processData: false, // Prevent jQuery from processing the data
          success: function(response) {
              console.log(response);
          },
          error: function(error) {
              //console.log('Error:', error);
          }
      });
      //alert("Done!")
      // Reset the form items
      //document.getElementById("registerForm").reset();
  });

  $('#sendOTP').click(function() {
    var email = $('#email').val();
    $('#otp').val("");
    $.ajax({
        url: '/sendotp/',
        method: 'GET',
        data: {
            email: email
        },
        success: function(response) {
            console.log(response)
            if (response === true){
                alert("Otp sent! Please Check Your Email")
            }
            else{
            alert(response.message)
            }
        },
        error: function(error) {
            console.log('Error:', error);
        }
    });
  });



  $('#loginForm').submit(function(event) {
    event.preventDefault(); // Prevent form submission

    var formData = new FormData(); // Create a FormData object

    // Append the form fields to the FormData object
    formData.append('email', $('#email').val());
    formData.append('password', $('#password').val());

    $.ajax({
        url: '/login/',
        method: 'POST',
        data: formData,
        contentType: false, // Prevent jQuery from setting content type
        processData: false, // Prevent jQuery from processing the data
        success: function(response) {
            console.log(response);
            if (response === true){
              window.location.href = "/home/";
            }
            else{
                window.location.href = "/login/";
            }
        },
        error: function(error) {
            //console.log('Error:', error);
        }
    });
    //alert("Done!")
    // Reset the form items
    //document.getElementById("registerForm").reset();
  });
});

function togglePasswordVisibility() {
  var passwordInput = document.getElementById("password");
  var toggleIcon = document.querySelector(".toggle-password i");

  if (passwordInput.type === "password") {
      passwordInput.type = "text";
      toggleIcon.classList.remove("fa-eye");
      toggleIcon.classList.add("fa-eye-slash");
  } else {
      passwordInput.type = "password";
      toggleIcon.classList.remove("fa-eye-slash");
      toggleIcon.classList.add("fa-eye");
  }
}

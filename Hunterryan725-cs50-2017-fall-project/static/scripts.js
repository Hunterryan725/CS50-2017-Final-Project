function validateForm() {
    var x = document.forms["registration"]["email"].value;
    if (x.includes("@yale.edu"))
    {
      return true;
    }
    else
    {
      alert("Email must be a Yale Email");
      return false;
    }
}

FB.getLoginStatus(function(response) {
    statusChangeCallback(response);
});

function checkLoginState() {
  FB.getLoginStatus(function(response) {
    statusChangeCallback(response);
  });
}

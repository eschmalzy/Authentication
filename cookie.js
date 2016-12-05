var register = document.getElementById("register");
var signInB = document.getElementById("sign-in-button");
var registerB = document.getElementById("register-button");
var title = document.getElementById("title");
var email = document.getElementById("email");
var password = document.getElementById("password");
var fname = document.getElementById("fname");
var lname = document.getElementById("lname");

register.onclick = function() {
  document.getElementById("signInBox").style.display = "none";
  document.getElementById("registerBox").style.display = "initial";
  title.innerText = "Register";
};

signInB.onclick = function() {
  email = document.getElementById("semail").value;
  password = document.getElementById("spassword").value;
  if (email == "" || password == ""){
    alert("Email and password required for login")
  } else {
    signIn(function(){
      email.value = "";
      password.value = "";
      alert("Welcome back, "+email);
      document.getElementById("contacts").style.display = "block";
      document.getElementById("signInBox").style.display = "none";
      document.getElementById("registerBox").style.display = "none";
      populate();
    }, function(){
      alert("Invalid Username or Password");
      console.log("Couldn't log in");
    });
  }
};

registerB.onclick = function(){
  email = document.getElementById("remail").value;
  password = document.getElementById("rpassword").value;
  fname = document.getElementById("fname").value;
  lname = document.getElementById("lname").value;
  if (email == "" || password == ""){
    alert("Invalid username or password")
  } else{
    addUser(function(){
      email.value = "";
      password.value = "";
      fname.value = "";
      lname.value = "";
      document.getElementById("signInBox").style.display = "initial";
      document.getElementById("registerBox").style.display = "none";
      title.innerText = "Sign In";
    },function(){
      alert("had issues registering");
    })
  }
}

var addUser = function (success, failure){
  var post = new XMLHttpRequest();
  post.onreadystatechange = function (){
    if (post.readyState == XMLHttpRequest.DONE){
      if (post.status >= 200 && post.status < 400) {
        users = JSON.parse(post.responseText);
        success();
      } else {
        failure();
      }
    }
  };
  console.log(email);
  console.log(password);
  console.log(fname);
  console.log(lname);
  post.open("POST", "http://localhost:8080/users");
  post.withCredentials = true;
  post.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  post.send("email="+email+"&encryptedpass="+password+"&fname="+fname+"&lname="+lname);
};


var signIn = function(success, failure){
  var request = new XMLHttpRequest();
  request.onreadystatechange = function (){
    if (request.readyState == XMLHttpRequest.DONE){
      if (request.status >= 200 && request.status < 400) {
        user = JSON.parse(request.responseText);
        success();
      } else {
        failure();
      }
    }
  };
  request.open("POST", "http://localhost:8080/sessions");
  request.withCredentials = true;
  request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  request.send("email="+email+"&encryptedpass="+password);
};

function populate(){
  var request = new XMLHttpRequest();
  request.onreadystatechange = function (){
    if (request.readyState == XMLHttpRequest.DONE){
      if (request.status >= 200 && request.status < 400) {
        contacts = JSON.parse(request.responseText);
        console.log("Contacts Loaded");
        count = 0;
        for (var i = 0, len = contacts.length; i <len; i++){
          printcontacts(contacts[i]);
        }
      } else {
        console.error("Couldn't load contacts!");
        document.getElementById("signInBox").style.display = "initial";
        document.getElementById("contacts").style.display = "none";
      }
    }
  };
request.open("GET", "http://localhost:8080/contacts");
request.withCredentials = true;
request.send();
};

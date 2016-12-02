var saveButton = document.getElementById("save-button");
var name = document.getElementById('name');
var phone = document.getElementById('phone');
var email = document.getElementById('email');
var age = document.getElementById('age');
var birthday = document.getElementById('birthday');
var address = document.getElementById('address');
var editpress = false;
var editIndex = -1;
var deletes = [];
var reduce = 0;

document.getElementById("name")
    .addEventListener("keyup", function(event) {
    event.preventDefault();
    if (event.keyCode == 13) {
        document.getElementById("save-button").click();
    }
});


saveButton.onclick = function (){
  name = document.getElementById('name').value
  phone = document.getElementById('phone').value
  email = document.getElementById('email').value
  age = document.getElementById('age').value
  birthday = document.getElementById('birthday').value
  address = document.getElementById('address').value
  if (editpress){
    reduce = 0;
    for(var j = 0; j < deletes.length; j++){
      if (deletes[j] < editIndex){
        reduce += 1;
      }
    }

    document.getElementById('contact-list').children[editIndex].innerHTML = document.getElementById("name").value+"</br>" + document.getElementById('phone').value +"</br>" + "<button onclick='edit_row("+currentContact['id']+")'>Edit</button><button onclick='delete_row("+currentContact['id']+")'>Delete</button></br>";
    currentContact['name'] = document.getElementById('name').value
    currentContact['phone'] = document.getElementById('phone').value
    currentContact['email'] = document.getElementById('email').value
    currentContact['age'] = document.getElementById('age').value
    currentContact['birthday'] = document.getElementById('birthday').value
    currentContact['address'] = document.getElementById('address').value
    updatecontact();
    editpress = false;
    document.getElementById('type').innerHTML = "New Contact";
    document.getElementById('name').value = "";
    document.getElementById('phone').value = "";
    document.getElementById('email').value = "";
    document.getElementById('age').value = "";
    document.getElementById('birthday').value = "";
    document.getElementById('address').value = "";
    return
  }
  addcontact(function(){
    console.log("Saved Contact")
    document.getElementById('name').value = "";
    document.getElementById('phone').value = "";
    document.getElementById('email').value = "";
    document.getElementById('age').value = "";
    document.getElementById('birthday').value = "";
    document.getElementById('address').value = "";
    getcontacts(function(contacts){
      console.log("Success");
        printcontacts(contacts[contacts.length-1]);
    },function(){
      console.error("Had a problem")
    });
  }, function(){
    console.error("Unable to save contact")
  })
}

var addcontact = function (success, failure){
  var post = new XMLHttpRequest();
  post.onreadystatechange = function (){
    if (post.readyState == XMLHttpRequest.DONE){
      if (post.status >= 200 && post.status < 400) {
        contacts = JSON.parse(post.responseText);
        success();
      } else {
        failure();
      }
    }
  };
  post.open("POST", "http://localhost:8080/contacts");
  post.withCredentials = true;
  post.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  post.send("name="+name+"&phone="+phone+"&email="+email+"&age="+age+"&birthday="+birthday+"&address="+address);
};

var count = 0;
function printcontacts(item){
  var lst = document.getElementById('contact-list');
  var c = document.querySelector("#contact");
  li = c.content.querySelectorAll("li");
  li[0].innerHTML = item['name']+"</br>" + item['phone'] +"</br>" + "<button onclick='edit_row("+item['id']+")'>Edit</button><button onclick='delete_row("+item['id']+")'>Delete</button></br>";
  var clone = document.importNode(c.content, true);
  lst.appendChild(clone);
  console.log(document.getElementById("contact-list"));
  if (editpress == false){
    count += 1;
  }
}

var getcontacts = function (success, failure){
  var request = new XMLHttpRequest();
  request.onreadystatechange = function (){
    if (request.readyState == XMLHttpRequest.DONE){
      if (request.status >= 200 && request.status < 400) {
        contacts = JSON.parse(request.responseText);
        success(contacts);
      } else {
        failure();
      }
    }
  };
  request.open("GET", "http://localhost:8080/contacts");
  request.withCredentials = true;
  request.send();
};

//on page load populate the list
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

populate();

var updatecontact = function (){
  var request = new XMLHttpRequest();
  request.onreadystatechange = function (){
    if (request.readyState == XMLHttpRequest.DONE){
      if (request.status >= 200 && request.status < 400) {
        contacts = JSON.parse(request.responseText);
        // success(contacts);
      } else {
        // failure();
      }
    }
  };
  request.open("PUT", "http://localhost:8080/contacts/"+currentContact['id'],true);
  request.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  request.send("name="+currentContact['name']+"&phone="+currentContact['phone']+"&email="+currentContact['email']+"&age="+currentContact['age']+"&birthday="+currentContact['birthday']+"&address="+currentContact['address']);
};

var deletecontact = function (success, failure){
  var request = new XMLHttpRequest();
  request.onreadystatechange = function (){
    if (request.readyState == XMLHttpRequest.DONE){
      if (request.status >= 200 && request.status < 400) {
        // contacts = JSON.parse(request.responseText);
        success();
      } else {
         failure();
      }
    }
  };
  request.open("DELETE", "http://localhost:8080/contacts/"+currentContact["id"], true);
  request.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  request.send();
};


var currentContact = -1;

function edit_row(i) {
    // if(!submitpress){
    //     submitpress = true;
    if (!editpress){
    getcontacts(function(contacts){
      console.log("Got contacts");
    },function(){
      console.error("Had a problem getting contacts")
    });
        editpress = true;
        var index = 0;
        for (var j in contacts)
        {
          if(contacts[j]['id'] == i){
              currentContact = contacts[j];
              editIndex = j;
              break;
            }
            index++;
        }
        // editIndex = contacts[j]['id'];
        document.getElementById('name').value = currentContact['name'];
        document.getElementById('phone').value = currentContact['phone'];
        document.getElementById('email').value = currentContact['email'];
        document.getElementById('age').value = currentContact['age'];
        document.getElementById('birthday').value = currentContact['birthday'];
        document.getElementById('address').value = currentContact['address'];
        document.getElementById('type').innerHTML = "Edit Contact";
    // }
  }else{
    editpress = false;
    document.getElementById('type').innerHTML = "New Contact";
    document.getElementById('name').value = "";
    document.getElementById('phone').value = "";
    document.getElementById('email').value = "";
    document.getElementById('age').value = "";
    document.getElementById('birthday').value = "";
    document.getElementById('address').value = "";
  }
}


function delete_row(index) {

    var result = confirm("Want to delete?");
    if(result){
    getcontacts(function(contacts){
      console.log("Got contacts");
    },function(){
      console.error("Had a problem getting contacts")
    });
    var deleteIndex;
    for (var c in contacts)
    {
      console.log(c);
      // console.log(contacts[Object.keys(contacts).length - 1]['id']);
      if(contacts[c]['id'] == index){
        currentContact = contacts[c];
        deleteIndex = c;
        break;
      }
    }
        var ul = document.getElementById("contact-list");
        deletecontact(function(contacts){
          console.log("Successful delete");
          if(!deletes.includes(deleteIndex)){
            deletes.push(deleteIndex)
          }
          reduce = 0;
          for(var j = 0; j < deletes.length; j++){
            if (deletes[j] < c){
              reduce += 1;
            }
          }
          ul.removeChild(ul.children[deleteIndex]);
          console.log("reduce " + reduce);
        },function(){
          console.error("Had a problem deleting!")
        });
      }
}

const firebaseConfig = {
    apiKey: "AIzaSyBe1HUnwUTeGJOIJDOq2Zs_nzlo07dWVqI",
    authDomain: "signup-app-3e9dc.firebaseapp.com",
    projectId: "signup-app-3e9dc",
    storageBucket: "signup-app-3e9dc.appspot.com",
    messagingSenderId: "50794442018",
    appId: "1:50794442018:web:b5603c5a46d0b7a815c97b"
};
  // initialize firebase
  firebase.initializeApp(firebaseConfig);
  
  // reference your database
  var contactFormDB = firebase.database().ref("sandy",);
  
  document.getElementById("contactForm").addEventListener("submit", submitForm);
  
  function submitForm(e) {
    e.preventDefault();
  
    var name = getElementVal("name");
    var emailid = getElementVal("emailid");
    var msgContent = getElementVal("msgContent");
  
    saveMessages(name, emailid, msgContent);
  
    //   enable alert
    document.querySelector(".alert").style.display = "block";
  
    //   remove the alert
    setTimeout(() => {
      document.querySelector(".alert").style.display = "none";
    }, 3000);
  
    //   reset the form
    document.getElementById("contactForm").reset();
  }
  
  const saveMessages = (name, emailid, msgContent) => {
    var newContactForm = contactFormDB.push();
  
    newContactForm.set({
      name: name,
      emailid: emailid,
      msgContent: msgContent,
    });
  };
  
  const getElementVal = (id) => {
    return document.getElementById(id).value;
  };
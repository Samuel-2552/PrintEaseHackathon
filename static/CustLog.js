// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.19.1/firebase-app.js";
import { getDatabase, set, ref } from "https://www.gstatic.com/firebasejs/9.19.1/firebase-database.js";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword, sendEmailVerification, sendPasswordResetEmail, fetchSignInMethodsForEmail } from "https://www.gstatic.com/firebasejs/9.19.1/firebase-auth.js";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyBe1HUnwUTeGJOIJDOq2Zs_nzlo07dWVqI",
    authDomain: "signup-app-3e9dc.firebaseapp.com",
    projectId: "signup-app-3e9dc",
    storageBucket: "signup-app-3e9dc.appspot.com",
    messagingSenderId: "50794442018",
    appId: "1:50794442018:web:b5603c5a46d0b7a815c97b"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

const database = getDatabase(app);
const auth = getAuth();

// popup variable
const popupBox = document.getElementById('popup-box');
const popupMessage = document.getElementById('popup-message');
const popupClose = document.getElementById('popup-close');

//integrated pop up for signup
signup.addEventListener('click', (e) => {

    var username = document.getElementById('Susername').value;
    var password = document.getElementById('Spassword').value;
    var email = document.getElementById('Semail').value;

    const auth = getAuth();
    fetchSignInMethodsForEmail(auth, email)
        .then((signInMethods) => {
            if (signInMethods.length > 0) {
                // User already exists, show pop-up and open login card
                popupMessage.innerHTML = "User already exists. Please log in!";
                popupBox.style.display = "block";
                setTimeout(() => {
                    popupBox.style.display = "none";
                }, 5000);

                const loginCheckbox = document.getElementById('chk');
                loginCheckbox.checked = true;
            } else {
                // User doesn't exist, create new user
                createUserWithEmailAndPassword(auth, email, password)
                    .then((userCredential) => {
                        const user = userCredential.user;
                        popupMessage.innerHTML = "User created!";
                        popupBox.style.display = "block";
                        setTimeout(() => {
                            popupBox.style.display = "none";
                        }, 5000);

                        set(ref(database,'users/' + username.value),{
                            username: username,
                            email_id:email
                        })
                        //opening the login card
                        const loginCheckbox = document.getElementById('chk');
                        loginCheckbox.checked = true;
                        // Clear the input fields
                        document.getElementById('Susername').value = '';
                        document.getElementById('Semail').value = '';
                        document.getElementById('Spassword').value = '';
                    })
                    .catch((error) => {
                        const errorCode = error.code;
                        const errorMessage = error.message;
                        popupMessage.innerHTML = errorMessage;
                        popupBox.style.display = "block";
                        setTimeout(() => {
                            popupBox.style.display = "none";
                        }, 5000);
                    });
            }
        })
        .catch((error) => {
            const errorCode = error.code;
            const errorMessage = error.message;
            popupMessage.innerHTML = errorMessage;
            popupBox.style.display = "block";
            setTimeout(() => {
                popupBox.style.display = "none";
            }, 5000);
        });
});

// modified forgot password to integrate pop up
forgotpassword.addEventListener('click', (e) => {
    var email = document.getElementById('Lemail').value;
    if (email) {
        const auth = getAuth();
        fetchSignInMethodsForEmail(auth, email).then((signInMethods) => {
            if (signInMethods.length > 0) {
                // Email exists, send password reset email
                sendPasswordResetEmail(auth, email)
                    .then(() => {
                        popupMessage.innerHTML = "Password reset link sent successfully!"
                        popupBox.style.display = "block";
                        setTimeout(() => {
                            popupBox.style.display = "none";
                        }, 5000);
                    })
                    .catch((error) => {
                        const errorCode = error.code;
                        const errorMessage = error.message;
                        popupMessage.innerHTML = errorMessage;
                        popupBox.style.display = "block";
                        setTimeout(() => {
                            popupBox.style.display = "none";
                        }, 5000);
                    });
            } else {
                // Email does not exist
                popupMessage.innerHTML = "Email does not exist. Please Sign Up!"
                popupBox.style.display = "block";
                setTimeout(() => {
                    popupBox.style.display = "none";
                }, 5000);
            }
        }).catch((error) => {
            const errorCode = error.code;
            const errorMessage = error.message;
            popupMessage.innerHTML = errorMessage;
            popupBox.style.display = "block";
            setTimeout(() => {
                popupBox.style.display = "none";
            }, 5000);
        });
    } else {
        popupMessage.innerHTML = "Please enter your email!"
        popupBox.style.display = "block";
        setTimeout(() => {
            popupBox.style.display = "none";
        }, 5000);
    }
});


popupClose.addEventListener('click', () => {
    if (popupBox) {
        popupBox.style.display = "none";
    }
});


// added pop up for login also
login.addEventListener('click', (e) => {

    var email = document.getElementById('Lemail').value;
    var password = document.getElementById('Lpassword').value;

    const auth = getAuth();
    fetchSignInMethodsForEmail(auth, email)
        .then((signInMethods) => {
            if (signInMethods.length > 0) {
                signInWithEmailAndPassword(auth, email, password)
                    .then((userCredential) => {
                        // Signed in 
                        document.getElementById('Lemail').value = '';
                        document.getElementById('Lpassword').value = '';
                        const user = userCredential.user;
                        popupMessage.innerHTML = "User logged in!";
                        popupBox.style.display = "block";
                        setTimeout(() => {
                            popupBox.style.display = "none";
                        }, 5000);
                        console.log("email verification: " + user.emailVerified);
                    })
                    .catch((error) => {
                        const errorCode = error.code;
                        const errorMessage = error.message;
                        popupMessage.innerHTML = errorMessage;
                        popupBox.style.display = "block";
                        setTimeout(() => {
                            popupBox.style.display = "none";
                        }, 5000);
                    });
            } else {
                const loginCheckbox = document.getElementById('chk');
                        loginCheckbox.checked = false;
                popupMessage.innerHTML = "User does not exist. Please Sign Up!";
                popupBox.style.display = "block";
                setTimeout(() => {
                    popupBox.style.display = "none";
                }, 5000);
            }
        })
        .catch((error) => {
            const errorCode = error.code;
            const errorMessage = error.message;
            popupMessage.innerHTML = errorMessage;
            popupBox.style.display = "block";
            setTimeout(() => {
                popupBox.style.display = "none";
            }, 5000);
        });

});
// getElementById() methods

const identity = document.getElementById("identity");
const firstName = document.getElementById("firstname");

// Functions

function welcomeUser() {
    let person = firstname.value;
    document.getElementById("welcome").innerHTML = "Welcome " + person + "!";
    localStorage.setItem("user", person);
  }

function welcomeBackUser() {
    let person = localStorage.getItem("user");
    document.getElementById("welcome").innerHTML = "Welcome back, " + person + "!";
}

// Calling the correct function depending on the local storage being empty or storing a value

if (localStorage.getItem("user") === null) {
    identity.addEventListener("click", welcomeUser);
} else {
    welcomeBackUser();
}

// Cleaning the local storage for testing purposes:
// localStorage.clear();
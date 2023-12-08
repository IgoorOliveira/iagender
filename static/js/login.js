import { validateEmail, validatePassword } from "./validate.js";
const loginButton = document.querySelector(".login-button");

function updateStyleInput(typeInput, situation) {
    document.querySelector(`.input-${typeInput}`).classList.add(`input-${situation}`);
}

function resetStyleInput(user) {
    Object.keys(user).forEach((typeInput) =>{
        document.querySelector(`.input-${typeInput}`).classList.remove("input-sucess", "input-error");
    })
}

loginButton.addEventListener("click", (ev) =>{
    if(!loginIsValid()) ev.preventDefault()
})


export function loginIsValid() {
    
    const user = {
        "email": document.querySelector(".input-email").value.trim(),
        "password": document.querySelector(".input-password").value.trim()
    }
    resetStyleInput(user);

    const isValidEmail = validateEmail(user.email);
    const isValidPassword = validatePassword(user.password)
    


    updateStyleInput("email", `${isValidEmail? "sucess": "error"}`);
    updateStyleInput("password", `${isValidPassword? "sucess": "error"}`);

    return isValidEmail && isValidPassword;

} 





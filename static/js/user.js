import { validateEmail, validateName, validatePassword } from "./validate.js";

function updateStyleInput(typeInput, situation) {
    document.querySelector(`.input-${typeInput}`).classList.add(`input-${situation}`);
}

function resetStyleInput(user) {
    Object.keys(user).forEach((typeInput) =>{
        document.querySelector(`.input-${typeInput}`).classList.remove("input-sucess", "input-error");
    })
}

export function validateFormUser() {
    const user = {
        "name": document.querySelector(".input-name").value.trim(),
        "email": document.querySelector(".input-email").value.trim(),
        "password": document.querySelector(".input-password").value.trim()
    }
    resetStyleInput(user);

    const isValidName = validateName(user.name);
    const isValidEmail = validateEmail(user.email);
    const isValidPassword = validatePassword(user.password)

    updateStyleInput("name", `${isValidName? "sucess": "error"}`);
    updateStyleInput("email", `${isValidEmail? "sucess": "error"}`);
    updateStyleInput("password", `${isValidPassword? "sucess": "error"}`);

    
    return isValidName && isValidEmail && isValidPassword;

} 





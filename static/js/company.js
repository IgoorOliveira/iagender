import { validateUserUrl, validatePhone } from "./validate.js";
function updateStyleInput(typeInput, situation) {
    document.querySelector(`.input-${typeInput}`).classList.add(`input-${situation}`);
}

function resetStyleInput(company) {
    Object.keys(company).forEach((typeInput) =>{
        document.querySelector(`.input-${typeInput}`).classList.remove("input-sucess", "input-error");
    })
}

export function validateFormCompany() {
    
    const company = {
        "company": document.querySelector(".input-company").value.trim(),
        "user": document.querySelector(".input-user").value.trim(),
        "phone": document.querySelector(".input-phone").value.trim()
    };
    resetStyleInput(company)

    const isValidUserUrl = validateUserUrl(company.user)
    const isValidPhone = validatePhone(company.phone);
    updateStyleInput("user", `${isValidUserUrl? "sucess": "error"}`);
    updateStyleInput("phone", `${isValidPhone? "sucess": "error"}`);

    return isValidPhone;
}

function maskPhone(ev) {
    const phone = ev.target;
    const clearPhone = phone.value.replace(/\D/g, "").substring(0, 11);
    const listPhone = clearPhone.split("");
    
    let formatPhone = "";
    if(ev.key !== "Backspace") {
        if(listPhone.length > 0) {
            formatPhone += `(${listPhone.slice(0,2).join("")})`
        }
        
        if(listPhone.length > 2) {
            formatPhone += ` ${listPhone.slice(2,7).join("")}`
        }
        
        if(listPhone.length > 7) {
            formatPhone += `-${listPhone.slice(7,11).join("")}`
        }
        phone.value = formatPhone;
    }
}
document.querySelector(".input-phone").addEventListener("keyup", (ev) => maskPhone(ev));
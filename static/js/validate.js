
export function validateName(name) {
    return name.length > 4 && name.split(" ").length > 1;
}

export function validateEmail(email) {
    const regexEmail = /^[\w\.]{2,}@[a-zA-Z]{2,}\.[a-zA-Z]{2,}/g
    return regexEmail.test(email);
}

export function validatePassword(password) {
    return password.match(/^(?=.*[A-Z])(?=.*\d).{8,}$/);
} 


export function validatePhone(phone) {
    const regexPhone = /^\(\d{2}\) \d{5}-\d{4}$/;
    return regexPhone.test(phone);
}
export function validateUserUrl(user) {
    return user !== "" && user.split(" ").length == 1;
}


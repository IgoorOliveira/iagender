import {validateForm}  from "./authStep1.js";
import {validateForm3}  from "./authStep3.js";

const nextButtons = document.querySelectorAll(".next-button");
const backButtons = document.querySelectorAll(".back-button");
const qtySteps = 4;
let currentFormStep = Number(localStorage.getItem("currentFormStep") || 1);

function recoverLastForm() {
    document.querySelector(`.form-register-step${currentFormStep}`).classList.toggle("hidden");
    for (let index = 1; index <= currentFormStep; index++) {
        document.querySelector(`.bar-icon-step${index}`).classList.add("stroke-white", "fill-primary");
    }
}

function showNextForm() {
    document.querySelector(`.form-register-step${currentFormStep}`).classList.toggle("hidden");
    document.querySelector(`.form-register-step${currentFormStep + 1}`).classList.toggle("hidden");
}

function showLastForm() {
    document.querySelector(`.form-register-step${currentFormStep}`).classList.toggle("hidden");
    document.querySelector(`.form-register-step${currentFormStep - 1}`).classList.toggle("hidden");
}

function advanceProgressBar() {
    document.querySelector(`.bar-icon-step${currentFormStep + 1}`).classList.add("stroke-white", "fill-primary");
}

function returnProgressBar() {
    document.querySelector(`.bar-icon-step${currentFormStep}`).classList.remove("stroke-white", "fill-primary");
}

function handleNextButton() {
    const validateForms = {
            1: validateForm,
            2: validateForm,
            3: validateForm3,
            4: validateForm
        }
        if(currentFormStep < qtySteps) {
            
            if(validateForms[currentFormStep]()) {

                this.classList.add("active-spinner");

                setTimeout(() =>{
                    showNextForm();
                    advanceProgressBar();
                    currentFormStep += 1;
                    localStorage.setItem("currentFormStep", currentFormStep);
                    this.classList.remove("active-spinner");
                    
                }, 500)
            } else {
                event.preventDefault()
            }  
        }
}

for(const nextButton of nextButtons) {
    nextButton.addEventListener("click", handleNextButton);
}
document.addEventListener("keydown", (ev) => {
    if(ev.key == "Enter") {
        ev.preventDefault();
    }
})

for(const backButton of  backButtons) {
    backButton.addEventListener("click", ()=>{
        if(currentFormStep > 1) {
            showLastForm();
            returnProgressBar();
            currentFormStep -= 1;
            localStorage.setItem("currentFormStep", currentFormStep);
        }
    })
}

document.addEventListener("DOMContentLoaded", recoverLastForm);



const categoriesCards = document.querySelectorAll(".card-category");

for (const categoryCard of categoriesCards) {
    categoryCard.addEventListener("click", ()=>{
        disableStyleButton();
        categoryCard.classList.add("active-category");
    })
}

function disableStyleButton() {
    categoriesCards.forEach((categoryCard) =>{
        categoryCard.classList.remove("active-category");
    })
}

const nextButton = document.querySelector(".next-button")
const backButton = document.querySelector(".back-button")

const formTitle = document.querySelector(".form-title");
const formSubtitle = document.querySelector(".form-subtitle");
let currentFormStep = 1;


const textFormStep = {
    1: {
        "title": "Informações pessoais ",
        "subtitle": "Comece por nos contar um pouco sobre você"
    },
    2: {
        "title": "Informações cadastrais ",
        "subtitle": "Protegendo a sua conta"
    },
    3: {
        "title": "Informações cadastrais",
        "subtitle": "Como podemos entrar em contato com você?"
    },
    4: {
        "title": "Localização",
        "subtitle": "Como podem encontrar você?"
    },
    5: {
        "title": "Agenda",
        "subtitle": "Escolha o horário que se adapta a sua rotina"
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

function showStepText() {
    formTitle.innerText = textFormStep[currentFormStep]["title"];
    formSubtitle.innerText = textFormStep[currentFormStep]["subtitle"];
}

function advanceProgressBar() {
    document.querySelector(`.bar-progress-step${currentFormStep}`).classList.toggle("hidden");
    document.querySelector(`.bar-progress-step${currentFormStep + 1}`).classList.toggle("hidden");
    document.querySelector(`.bar-progress-step${currentFormStep }`).parentElement.classList.toggle('active-bar');
    document.querySelector(`.bar-progress-step${currentFormStep + 1}`).parentElement.classList.toggle('active-bar');
    document.querySelector(`.bar-icon-step${currentFormStep + 1}`).classList.add("fill-primary", "stroke-white");
}

function returnProgressBar() {
    document.querySelector(`.bar-progress-step${currentFormStep}`).classList.toggle("hidden");
    document.querySelector(`.bar-progress-step${currentFormStep - 1}`).classList.toggle("hidden");
    document.querySelector(`.bar-progress-step${currentFormStep }`).parentElement.classList.toggle('active-bar');
    document.querySelector(`.bar-progress-step${currentFormStep - 1}`).parentElement.classList.toggle('active-bar');
    document.querySelector(`.bar-icon-step${currentFormStep}`).classList.remove("fill-primary", "stroke-white");
}

nextButton.addEventListener("click", ()=>{
    const spinButton = document.querySelector(".button-spin");
    nextButton.classList.add("hidden");
    spinButton.classList.remove("hidden");
    setTimeout(() => {
        nextButton.classList.remove("hidden");
        spinButton.classList.add("hidden");
        showNextForm();
        advanceProgressBar()
        currentFormStep += 1;
        showStepText(); 
    }, 500);

     
})
backButton.addEventListener("click", ()=>{
    if(currentFormStep > 1) {
        showLastForm();
        returnProgressBar()
        currentFormStep -= 1;
        showStepText();
    }
    
})



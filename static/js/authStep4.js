const adress = {
    "cep": document.querySelector(".input-cep"),
    "logradouro": document.querySelector(".input-logradouro"),
    "city": document.querySelector(".input-city"),
    "uf": document.querySelector(".input-state"),
    "number": document.querySelector(".input-number"),
    "neighborhood": document.querySelector(".input-neighborhood"),
    "complement": document.querySelector(".input-complement")
};

const errorAlertCep = document.querySelector(".error-alert-cep");


async function fetchAdress(cep) {
    return await fetch(`https://viacep.com.br/ws/${cep}/json/`).then(result => result.json());
}

async function getAdress(cep) {
    const data = await fetchAdress(cep)
    renderAdress(data)
}

function renderAdress(data) {

    if(!("erro" in data)) {
        const {logradouro, localidade, uf, bairro} = data;
        adress.logradouro.value = logradouro;
        adress.city.value = localidade
        adress.uf.value = uf
        adress.neighborhood.value = bairro
    } else {
        clearFields();
        errorAlertCep.innerText = "CEP não encontrado!";
    }
    
}

function clearFields() {
    adress.cep.value = "";
    adress.logradouro.value = "";
    adress.city.value = ""
    adress.uf.value = "";
    adress.neighborhood.value = "";
    adress.complement.value = ""
}

function validateCep() {
    adress.cep.value = adress.cep.value.replace(/\D/g, '')
    const regexCep = /^[0-9]{8}$/;

    if(regexCep.test(adress.cep.value)) {
        getAdress(adress.cep.value)

    } else {
        errorAlertCep.innerText = "Preencha o CEP corretamente!";
        updateStyleInput("cep", "error");
        clearFields();
    }
}
adress.cep.addEventListener("blur", validateCep);
adress.cep.addEventListener("focus", ()=>{
    errorAlertCep.innerText = "";
    adress.cep.classList.remove("input-error");
})

export function validateFormAdress() {
    let validate = true
    Object.keys(adress).forEach(typeInput => {
        if (typeInput !== "complement" && adress[typeInput].value === "") {
            validate = false;
        }
    })
    return validate
}
function updateStyleInput(typeInput, situation) {
    adress[typeInput].classList.add(`input-${situation}`);
}


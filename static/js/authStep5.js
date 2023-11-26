
function createHoursIntervalFieldComponent(day) {
    const hoursIntervalField = document.createElement("div");
    hoursIntervalField.classList.add("w-[90%]", "flex", "items-center", "gap-2")
    const inputOpen = createSelectTimeComponent("09:00")
    const inputClose = createSelectTimeComponent("18:00")
    const p = document.createElement("p").innerText = "Até"
    inputOpen.name = `initial_interval_${day.toLowerCase()}`
    inputClose.name = `close_interval_${day.toLowerCase()}`

    hoursIntervalField.append(inputOpen, p, inputClose);
    return hoursIntervalField
}

function getTime(initialHour, finalHour, intervalMin) {
    const listTime = [];
    let currentTime = initialHour * 60;
    const finalMin = finalHour * 60;

    while (currentTime <= finalMin) {
        const hours = String(Math.floor(currentTime / 60)).padStart(2, '0');
        const minutes = String(currentTime % 60).padStart(2, '0');
        listTime.push(`${hours}:${minutes}`);
        currentTime += intervalMin;
    }

    return listTime;
}


function createSelectTimeComponent(valueStandardSelected) {
    const select = document.createElement("select");
    select.classList.add("rounded-lg", "w-1/2")
    const listOption = []
    const listTime = getTime(0, 23, 15);

    listTime.forEach(time =>{
        const option = document.createElement("option");
        option.innerText = time;
        option.value = time;

        if(time == valueStandardSelected) option.selected = true
        listOption.push(option);
    })

    select.append(...listOption);
    return select
}

function createRowFieldsComponent(day){
    const row = document.createElement("div");
    row.classList.add("flex", "justify-between");
    const intervalComponent = createHoursIntervalFieldComponent(day);
    const trashIcon = createTrashIcon();
    row.append(intervalComponent, trashIcon);
    return row;
}


function createAddFieldsIcon() {
    const icon = document.createElement("img");
    icon.src = `../static/assets/svg/plus-circle.svg`;

    icon.classList.add("cursor-pointer", "add-fields");
    icon.addEventListener("click", () =>{
        const day = icon.closest(".fields-days").id
        const rowFields = createRowFieldsComponent(day);
        const fieldHours = icon.closest('.fields-hours');
        fieldHours.append(rowFields);
    })
    return icon;
}

function createTrashIcon(){
    const icon = document.createElement("img");
    icon.src = `../static/assets/svg/trash.svg`
    icon.style.cursor = "pointer"

    icon.addEventListener("click", () =>{
        row = icon.parentNode
        row.remove()
    })
    return icon;
}




const arrowsDetails = document.querySelectorAll(".arrow-details");

for (const arrowDetails of arrowsDetails) {
    arrowDetails.addEventListener("click", () =>{
        toggleFieldsHours(arrowDetails)
    })
}

const toggleInputs = document.querySelectorAll('.toggle-input');


for(const toggleInput of toggleInputs) {
    toggleInput.addEventListener('change', () => {
        const fieldsDays = toggleInput.closest(".fields-days");
        const toggleButtonDay = toggleInput.parentElement

        const toggleLabel = toggleButtonDay.querySelector(".toggle-label");
        const toggleHandle = toggleButtonDay.querySelector(".toggle-handle");

        toggleHandle.classList.toggle("toggle-checked");
        toggleLabel.classList.toggle("bg-primary");

        if(toggleInput.checked) {
            openFieldsHours(toggleInput)
        } else {
            closeFieldsHours(toggleInput)
        }
        
        fieldsDays.classList.toggle("day-open");

});
}

function closeFieldsHours(button) {
    const box = button.closest(".fields-days");
    box.classList.remove("show-fields-hours");
}

function openFieldsHours(button) {
    const box = button.closest(".fields-days");
    box.classList.add("show-fields-hours");
}
function toggleFieldsHours(button) {
    const box = button.closest(".fields-days");
    box.classList.toggle("show-fields-hours");
}


document.addEventListener("DOMContentLoaded", () =>{
    const fieldsHours = document.querySelectorAll(".fields-hours");
    fieldsHours.forEach(field =>{
        const row = document.createElement("div");
        row.classList.add("flex", "justify-between");
        const day = field.closest(".fields-days").id
        console.log(day)
        const intervalComponent = createHoursIntervalFieldComponent(day);
        const addFieldsIcon = createAddFieldsIcon();
        row.append(intervalComponent, addFieldsIcon);
        field.append(row)
    })
})
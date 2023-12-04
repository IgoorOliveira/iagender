const calendarDays = document.querySelector(".days");
const nextMonthButton = document.querySelector(".next-month-button");
const prevMonthButton = document.querySelector(".prev-month-button");
const nextDayButton = document.querySelector(".next-day-button");
const prevDayButton = document.querySelector(".prev-day-button");
const timeContainer = document.querySelector(".time-container");
const month = document.querySelector(".month");
const date = getDate()
let daysWithSchedule = {
    "days": []
}
const months = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"];

const day_of_week = {
    1: "Segunda",
    2: "Terça",
    3: "Quarta",
    4: "Quinta",
    5: "Sexta",
    6: "Sábado",
    7: "Domingo"
}

const fetchDaysWithSchedule = async () =>{
    const paramUrl = getParametersUrl()

    return await fetch(`http://127.0.0.1:8000/days-with-schedule/${paramUrl.date}`).then(res => res.json())
}

const getDaysWithSchedule = async () => {
    const res = await fetchDaysWithSchedule();
    daysWithSchedule["days"] = res["days_with_schedule"];
    console.log(res["days_with_schedule"])
    renderCalendar();
    renderDay();

}

const renderCalendar = () =>{
    const days = []
    let currentMonth = date.getMonth()
    const currentYear = date.getFullYear()

    const today = date.getDate()
    const firstDayIndex = new Date(currentYear, currentMonth, 1).getDay()

    const lastIndexLastMonth = new Date(currentYear, currentMonth, 0).getDate()
    const lastDayThisMonth = new Date(currentYear, currentMonth + 1, 0).getDate()

    
    month.innerText = `${months[currentMonth]} ${currentYear}`

    for (let i = firstDayIndex; i > 0; i--) {
        days.push(createDayComponent(lastIndexLastMonth - i + 1, "prev-days"))
    }

    for (let x = 1; x <= lastDayThisMonth; x++) {
        if (x === today && date.getMonth() === new Date().getMonth() && date.getFullYear() === new Date().getFullYear()) {
            days.push(createDayComponent(x, "current-days"));
        } else {
            days.push(createDayComponent(x, "current-days"))
        }
    }


    days.forEach(day =>{
        calendarDays.appendChild(day)
    })
}

function createDayComponent(value, style) {
    const day = document.createElement("a");
    day.classList.add("day", style);
    day.innerText = value;
    if(style == "current-days") {
        if(daysWithSchedule["days"].includes(value)) {
            day.classList.add("days-with-service");
        }
    } 
    day.href = `${window.location.origin}/schedule/${date.getFullYear()}-${date.getMonth() + 1}-${value}`
    return day;
}


function getDate() {
    const url = window.location.href;
    const urlParts = url.split("/");
    
    const date = urlParts[urlParts.length - 1].split("-")
    const [year, month, day] = date
    
    return new Date(year, month - 1, day);
}


function renderDay() {
    const dayTitle = document.querySelector(".day-title");
    const year = date.getFullYear()
    let month = date.getMonth()
    const day = date.getDate()
    dayTitle.innerText = `${day_of_week[date.getDay() + 1]}, ${day} de ${months[month].toLowerCase()} ${year}`
}


function ModifyUrl(year = date.getFullYear(), month=date.getMonth(), day=date.getDate()) {
    const url = window.location.href;
    const urlParts = url.split("/");

    urlParts[urlParts.length - 1] = `${year}-${month + 1}-${day}`;
    
    const newUrl = urlParts.join("/");
    
    window.location.href = newUrl
}

function getParametersUrl() {

    const url = window.location.href;
    const urlParts = url.split("/");
    const date = urlParts[urlParts.length - 1];

    const paramUrl = {
        "date": date
    }

    return paramUrl

}

prevMonthButton.addEventListener("click", () =>{
    if(date.getMonth() === new Date().getMonth() && date.getFullYear() === new Date().getFullYear()) return

    date.setMonth(date.getMonth() - 1);
    ModifyUrl()
    getOperatingDays()
})
nextMonthButton.addEventListener("click", () =>{
    date.setMonth(date.getMonth() + 1);
    ModifyUrl()
    getOperatingDays()
})

prevDayButton.addEventListener("click", ()=> {

    date.setDate(date.getDate() - 1)
    ModifyUrl()
    getOperatingDays()
})

nextDayButton.addEventListener("click", ()=> {
    date.setDate(date.getDate() + 1)
    ModifyUrl()
    getOperatingDays()
})


getDaysWithSchedule()

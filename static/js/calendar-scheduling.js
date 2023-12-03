const calendarDays = document.querySelector(".days");
const nextMonthButton = document.querySelector(".next-month-button");
const prevMonthButton = document.querySelector(".prev-month-button");
const timeContainer = document.querySelector(".time-container");
const month = document.querySelector(".month");
const date = getDate()

let teste = {}
const months = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"];

const fetchOperatingDays = async () =>{
    const paramUrl = getParametersUrl()

    return await fetch(`http://127.0.0.1:8000/available_times/${paramUrl.username}/${paramUrl.service}/${paramUrl.date}`).then(res => res.json())
}

const getOperatingDays = async () => {
    const res = await fetchOperatingDays();
    teste = { ...res["operating_days"] };
    renderCalendar();
    renderTimes();
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

const renderTimes = (day = new Date().getDate()) =>{
    clearTimeButton()
    const listTimeButton = []

    if(!(day in teste)) {
        let num = 0
        for(const num of Object.keys(teste)) {
            if(num > day) {
                day = num
                break
            } 
        }
    }
    
    renderDay(day)
    teste[day].forEach(time  =>{
        listTimeButton.push(createTimeButton(time, day))
    })
    timeContainer.append(...listTimeButton)
}

const createTimeButton = (time, day) => {
    const timeButton = document.createElement("a");

    timeButton.classList.add("time-button");
    
    const icon = createIconTime(time)
    const timeText = document.createElement("p");
    timeText.innerText = time
    timeButton.addEventListener("click", () =>{
        window.location.href += `-${day}/${time}`
    })

    timeButton.append(icon, timeText)
    return timeButton
}



function createDayComponent(value, style) {
    const day = document.createElement("a");
    day.classList.add("day", style);
    day.innerText = value;

    if(style == "current-days") {
        if(value in teste) {
            day.classList.add("operating-day");
            day.addEventListener("click", () =>{
                renderTimes(value)
            })
        }
    
    } 
    return day;
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


function getParametersUrl() {
    const url = window.location.href

    const urlParts = url.split("/")
    const paramUrl = {
        "username": urlParts[4],
        "service": urlParts[5],
        "date": urlParts[6]

    }

    return paramUrl
}
getOperatingDays()

function ModifyUrl() {
    const url = window.location.href;
    const urlParts = url.split("/");
    const year = date.getFullYear();
    const month = date.getMonth();

    urlParts[urlParts.length - 1] = `${year}-${month + 1}`;
    
    const newUrl = urlParts.join("/");
    
    window.location.href = newUrl
}

function renderDay(day) {
    const dayTitle = document.querySelector(".day-title");
    const year = date.getFullYear()
    let month = date.getMonth()
    dayTitle.innerText = `${day} de ${months[month].toLowerCase()}, ${year}`
}

function getDate() {
    const url = window.location.href;
    const urlParts = url.split("/");
    
    const date = urlParts[urlParts.length - 1].split("-")
    const [year, month] = date
    
    return new Date(year, month - 1, 1)
}

function createIconTime(time) {
    const icon = document.createElement("img")
    const timeParts = time.split(":")
    const hour = timeParts[0]
    let icon_svg = ""
    if (hour >= 6 && hour < 12) {
        icon_svg = "sun";
    } else if (hour >= 12 && hour < 18) {
        icon_svg = "sun-cloud";
    } else {
        icon_svg = "moon";
    }

    icon.src = `../../../static/assets/svg/${icon_svg}.svg`;
    return icon
}

function clearTimeButton() {
    while(timeContainer.firstChild) {
        timeContainer.removeChild(timeContainer.firstChild);
    }
}

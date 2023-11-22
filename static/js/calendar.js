const calendarDays = document.querySelector(".days");
const nextMonthButton = document.querySelector(".next-month-button");
const prevMonthButton = document.querySelector(".prev-month-button");
const month = document.querySelector(".month");

const date = new Date()
const operating_days = []
const months = ["Janeiro", "Fevereiro", "Março", "Abril", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"];

const fetchOperatingDays = async () =>{
    return await fetch("http://127.0.0.1:8000/operating_days").then(res => res.json())
}

const getOperatingDays = async () =>{
    
    await fetchOperatingDays().then(res => {
        res.operating_days.forEach(day =>{
            operating_days.push(days_week[day])
        })
        renderCalendar()
    })
}

const days_week = {
    "Domingo": 0,
    "Segunda": 1,
    "Terça": 2,
    "Quarta": 3,
    "Quinta": 4,
    "Sexta": 5,
    "Sábado": 6
}

const renderCalendar = () =>{

    clearLastCalendar()
    const days = []
    let currentMonth = date.getMonth()
    const currentYear = date.getFullYear()

    const today = date.getDate()
    const firstDayIndex = new Date(currentYear, currentMonth, 1).getDay()

    const lastIndexLastMonth = new Date(currentYear, currentMonth, 0).getDate()
    const lastDayThisMonth = new Date(currentYear, currentMonth + 1, 0).getDate()
    const lastDayIndexMonth = new Date(currentYear, currentMonth + 1, 0).getDay()

    if(!months[currentMonth - 1]) currentMonth++
    month.innerText = `${months[currentMonth - 1]} ${currentYear}`

    for (let i = firstDayIndex; i > 0; i--) {
        days.push(createDayComponent(lastIndexLastMonth - i + 1, "prev-days"))
    }

    for (let x = 1; x <= lastDayThisMonth; x++) {
        if (x === today && date.getMonth() === new Date().getMonth() && date.getFullYear() === new Date().getFullYear()) {
            days.push(createDayComponent(x, "today"));
        } else {
            days.push(createDayComponent(x, "current-days"))
        }
    }

    for (let i = 1; i <= 7 - lastDayIndexMonth - 1; i++) {
        days.push(createDayComponent(i, "next-days"));
    }

    days.forEach(day =>{
        calendarDays.appendChild(day)
    })
}



function createDayComponent(value, style) {
    const day = document.createElement("button");
    if(style == "current-days" || style == "today") {
        const index = new Date(date.getFullYear(), date.getMonth(), value).getDay()
        
        if(operating_days.includes(index)) {
            day.classList.add("today");
        }
    }
    day.innerText = value;
    day.classList.add("cursor-pointer", "flex", "justify-center", "items-center", style);

    day.addEventListener("click", () =>{
        
    })
    return day;
}

function clearLastCalendar() {
    while(calendarDays.firstChild) {
        calendarDays.removeChild(calendarDays.firstChild);
    }
}
prevMonthButton.addEventListener("click", () =>{
    if(date.getMonth() === new Date().getMonth() && date.getFullYear() === new Date().getFullYear()) return

    date.setMonth(date.getMonth() - 1);
    renderCalendar()
})
nextMonthButton.addEventListener("click", () =>{
    date.setMonth(date.getMonth() + 1);
    renderCalendar()
})

renderCalendar();
getOperatingDays()
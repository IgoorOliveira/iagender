const calendarDays = document.querySelector(".days");
const nextMonthButton = document.querySelector(".next-month-button");
const prevMonthButton = document.querySelector(".prev-month-button");
const month = document.querySelector(".month");
const date = new Date()
const months = ["Janeiro", "Fevereiro", "Março", "Abril", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"];


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
    month.innerText = `${months[currentMonth - 1]} de ${currentYear}`


    for (let i = firstDayIndex; i > 0; i--) {
        days.push(createDayComponent(lastIndexLastMonth - i + 1, "prev-days"))
    }

    for (let x = 1; x <= lastDayThisMonth; x++) {
        if (x === today && date.getMonth() === new Date().getMonth()) {
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
    day.innerText = value;
    day.classList.add("cursor-pointer", "flex", "justify-center", "items-center", style);
    return day;
}

function clearLastCalendar() {
    while(calendarDays.firstChild) {
        calendarDays.removeChild(calendarDays.firstChild);
    }
}
prevMonthButton.addEventListener("click", () =>{
    date.setMonth(date.getMonth() - 1);
    renderCalendar()
})
nextMonthButton.addEventListener("click", () =>{
    date.setMonth(date.getMonth() + 1);
    renderCalendar()
})

renderCalendar();
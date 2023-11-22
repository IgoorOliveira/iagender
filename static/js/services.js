const createDurationComponent = () =>{
    const qty_fields = 10

    for (let i = 1; i <= qty_fields; i++) {
        const option = document.createElement("option");
        option.innerText = `${String(i).padStart(2, '0')}h`
        console.log(`${String(i).padStart(2, '0')}h`)
        document.querySelector(".service-duration").append(option)
    }

}
createDurationComponent()

const popupWrapper = document.querySelector(".popup-wrapper");
const registerServiceButton = document.querySelector(".register-service-button");
const closePopupButton = document.querySelector(".close-popup-button");




registerServiceButton.addEventListener("click", () =>{
    popupWrapper.classList.remove("hidden")
    popupWrapper.classList.add("flex")

})

closePopupButton.addEventListener("click", () =>{
    popupWrapper.classList.remove("flex")
    popupWrapper.classList.add("hidden")
})



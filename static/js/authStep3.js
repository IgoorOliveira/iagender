export function validateFormCategories() {
    const inputsCategories = document.querySelectorAll(".categories");
    for(const inputCategory of inputsCategories) {
        if(inputCategory.checked) return true
    }
    updateStyleCard()
    return false
}
function updateStyleCard() {
    const cardsCategories = document.querySelectorAll(".card-category");
    cardsCategories.forEach((cardCategory) =>{
        cardCategory.classList.add("alert-category");
        setTimeout(() => {
            cardCategory.classList.remove("alert-category");
        }, 2000);
    })
    
}
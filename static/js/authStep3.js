export function validateForm3() {
    const inputsCategories = document.getElementsByName("categories");
    for(const inputCategory of inputsCategories) {
        console.log(inputCategory)
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

const popup = document.getElementById("popup");
const popupContainer = document.getElementById("popup-container");
const yesButton = document.getElementById("yes-button");
const noButton = document.getElementById("no-button");

function showPopup() {
popup.style.display = "flex";
document.body.style.overflow = "hidden"; // disable scrolling
}

function hidePopup() {
popup.style.display = "none";
document.body.style.overflow = ""; // enable scrolling
}

yesButton.addEventListener("click", function () {
// do something if yes button is clicked
hidePopup();
});

noButton.addEventListener("click", function () {
// do something if no button is clicked
hidePopup();
});

showPopup();

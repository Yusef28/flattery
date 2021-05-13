// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var show_me_some_love_btn = document.getElementById("myBtn");
var flattering_words_p = document.getElementById("flattering_words_p");

// Get the <span> element that closes the modal
var close_modal_btn = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
show_me_some_love_btn.onclick = function() {

modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
close_modal_btn.onclick = function() {
  modal.style.display = "none";
  flattering_words_p.innerHTML = "";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "";
	flattering_words_p.innerHTML = "";
  }
}
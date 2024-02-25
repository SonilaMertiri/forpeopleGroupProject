var video = document.getElementById("myVideo");

// Remove the default controls
video.removeAttribute("controls");

// Add event listener to prevent right-click menu on the video
video.addEventListener("contextmenu", function(e) {
    e.preventDefault();
});
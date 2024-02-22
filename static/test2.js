// if (typeof gmap_key !== 'undefined' && gmap_key) {
//   const script = document.createElement('script');
//   script.src = `https://maps.googleapis.com/maps/api/js?key=AIzaSyDMKKvS9vRhP3fCiRPp42gK7-4bL2gYaMw&loading=async&callback=initMap`;
//   script.async = true;
//   document.head.appendChild(script);
// } else {
//   console.error("Google Maps API key is not available.");
// }
document.addEventListener('DOMContentLoaded', function () {
  initMap();
});

async function initMap() {
  var map = new google.maps.Map(document.getElementById('map'), {
      center: { lat: -34.397, lng: 150.644 },
      zoom: 8
  });

  const mapDiv = document.getElementById('map');
  const mapCenter = { lat: 53.3483031, lng: -6.2637067 };

  try {
      const { AdvancedMarkerElement } = await google.maps.importLibrary('marker');
      if (mapDiv) {
          map = new google.maps.Map(mapDiv, {
              center: mapCenter,
              zoom: 13
          });
      }
  } catch (error) {
      console.error('Error importing marker library:', error);
  }




// collapsable dropdown for weather info 
var weatherButton = document.getElementById("weatherButton");
if (weatherButton){
    weatherButton.addEventListener("click", function() {
        this.classList.toggle("active");

//code for changing icon weatherButton.style.backgroundImage = 'url(' + imageUrl + ')';//
        var weatherContent = this.nextElementSibling;
        if (weatherContent.style.display === "block") {
          weatherContent.style.display = "none";
        } else {
          weatherContent.style.display = "block";
        }
      })
    }

//get todays date
function getCurrentDate() {
  const today = new Date();
  const year = today.getFullYear();
  const month = String(today.getMonth() + 1).padStart(2, '0'); // Months are 0-based
  const day = String(today.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}


document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('dateInput').value = getCurrentDate();
})}

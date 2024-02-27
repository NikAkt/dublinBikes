let bikeStations = [];
let infoWindow;

// fetching the data from the api
async function fetchDublinBikesData() {
  try {
      const response = await fetch('https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=626c8de20316723c1526eed9a83479c9dd13f945');
      const data = await response.json();
      return data;
  } catch (error) {
      console.error('Error fetching Dublin Bikes data:', error);
      return null;
  }
}
//creating the markers using bike data
function createMarkers(map, bikeStations) {
  bikeStations.forEach(station => {
    const marker = new google.maps.Marker({
      position: station.position,
      map: map,
      title: station.name,  
    });
    marker.addListener('click', () => {
      if (infoWindow) {
          infoWindow.close(); 
      }
      infoWindow = new google.maps.InfoWindow({
          content: `<div>${station.name}<br>Available Bikes: ${station.available_bikes}</div>`
      });
      infoWindow.open(map, marker);
  });

  });
  
}
//function to update the markers every 5 mins
async function updateMarkers() {
  const updatedData = await fetchDublinBikesData();

  if (updatedData !== null) {
      bikeStations = updatedData;
      createMarkers(map, bikeStations);
      
  } else {
      console.error('Data not found.');
  }
}

// calling the init map function for displaying google map//
document.addEventListener('DOMContentLoaded', function () {
  initMap();
});
//the init map function for displaying google map
async function initMap() {
  var map = new google.maps.Map(document.getElementById('map'), {
      center: { lat: -34.397, lng: 150.644 },
      zoom: 8
  });
//setting the default display location of the map
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
      bikeStations = await fetchDublinBikesData();
      
// Create markers using the data
        createMarkers(map, bikeStations);

//populateDropdown
        populateDropdown('#startSelector select', bikeStations);
        populateDropdown('#destinationSelector select', bikeStations);
        

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

//get todays date and time
function getCurrentDateTime() {
  const today = new Date();
  const year = today.getFullYear();
  const month = String(today.getMonth() + 1).padStart(2, '0'); // Months are 0-based
  const day = String(today.getDate()).padStart(2, '0');
  const hours = String(today.getHours()).padStart(2, '0');
  const minutes = String(today.getMinutes()).padStart(2, '0');
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}


document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('dateTimeInput').value = getCurrentDateTime();
})}


//function to populate the dropwdowns with the stations
function populateDropdown(selector, stations) {
  const selectElement = document.querySelector(selector);
  selectElement.innerHTML = `<option value="">Select a Station</option>`;

  stations.forEach(station => {
    const option = document.createElement('option');
    option.value = `station${station.number}`;
    option.textContent = station.name;
    selectElement.appendChild(option);
  });
}
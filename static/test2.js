let bikeStations = [];
let infoWindow;
let availability;
// fetching the data from the api
async function fetchDublinBikesData() {
  try {
      const response=await fetch('/stations');
      const data=await response.json();
      stationData=data.station;
      return stationData;
  } catch (error) {
      console.error('Error fetching Dublin Bikes data:', error);
      return null;
  }
}
async function fetchAvailabilityBikesData() {
  try {
      const response=await fetch('/availability');
      const data=await response.json();
      availability=data.availability;
      temp=availability.reverse();
      availabilityActual=temp;
      return availabilityActual;
  } catch (error) {
      console.error('Error fetching availability data:', error);
      return null;
  }
}
//creating the markers using bike data
function createMarkers(map, bikeStations,availabilityActual) {
  console.log("hello",availabilityActual[0])
  for (let i = 0; i < bikeStations.length; i++) {
    const station = bikeStations[i];
    if (availabilityActual[i].available_bikes === 0) {
      markerColor = 'red';
    } else if (availabilityActual[i].available_bikes < 5) {
      markerColor = 'orange';
    } else if (availabilityActual[i].available_bikes < 10) {
      markerColor = 'green';
    } else {
      markerColor = 'blue';
    }
    const marker = new google.maps.Marker({
      position: {lat:station.position_lat, lng:station.position_lng},
      map: map,
      title: station.name,
      icon: {
        path: google.maps.SymbolPath.CIRCLE,
        fillColor: markerColor,
        fillOpacity: 1,
        strokeColor: '#FFFFFF', // Border color
        strokeWeight: 1, // Border width
        scale: 8 // Size of the marker
      }
    });
    marker.addListener('click', () => {
      if (infoWindow) {
          infoWindow.close(); 
      }
      infoWindow = new google.maps.InfoWindow({
          content: `<div>${station.name}<br>Available Bikes: ${availabilityActual[i].available_bikes}<br>Available Bike Stands: ${availabilityActual[i].available_bike_stands}</div>`
      });
      infoWindow.open(map, marker);
    });
  }
}
//function to update the markers every 5 mins
async function updateMarkers() {
  const updatedData = await fetchDublinBikesData();
  if (updatedData !== null) {
      bikeStations = updatedData;
      createMarkers(map, bikeStations,availabilityActual);
      
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
      // const { AdvancedMarkerElement } = await google.maps.importLibrary('marker');
      if (mapDiv) {
          map = new google.maps.Map(mapDiv, {
              center: mapCenter,
              zoom: 13
          });
      }
      bikeStations = await fetchDublinBikesData();
      availabilityActual= await fetchAvailabilityBikesData();
      
      // Create markers using the data
        createMarkers(map, bikeStations,availabilityActual);

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
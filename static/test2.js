let bikeStations = [];
const markers = [];
let infoWindow;
let availability;
let map;

const createMarkers = (map, bikeStations, availabilityActual) => {
  bikeStations.forEach((station, i) => {
    let markerColor;
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
      position: { lat: station.position_lat, lng: station.position_lng },
      map,
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
      const endSelector = document.querySelector('#destinationSelector select');
      endSelector.value = `station${station.number}`;
    });
    markers.push(marker); //adding each marker to markers array so it can be ecorporated in the cluster 
  });
  const markerCluster = new markerClusterer.MarkerClusterer({ markers, map }); //creating the cluster from markers
};

async function initMap() {
  //setting the default display location of the map
  const mapDiv = document.getElementById('map');
  const mapCenter = { lat: 53.3483031, lng: -6.2637067 };

  try {
      if (mapDiv) {
          map = new google.maps.Map(mapDiv, {
              center: mapCenter,
              zoom: 13,
              styles: [
                {
                  featureType: 'poi',
                  stylers: [{ visibility: 'off' }]
                },
                {
                  featureType: 'transit',
                  stylers: [{ visibility: 'off' }]
                },
                {
                  featureType: 'all',
                  stylers: [{ saturation: -30 }]
                }
              ],
              streetViewControl: false
          });
      
          const directionsService = new google.maps.DirectionsService();
          const directionsRenderer = new google.maps.DirectionsRenderer({
            polylineOptions: {
              strokeColor: 'magenta'
            }
          });
          directionsRenderer.setMap(map);

          const startSelector = document.querySelector('#startSelector select');
          
          const endSelector = document.querySelector('#destinationSelector select');
          const goButton = document.getElementById('goButton');

          goButton.addEventListener('click', function() {
            const startStationNumber = startSelector.value.replace('station', '');
            const startStation = bikeStations.find(station => station.number == startStationNumber);
          
            const endStationNumber = endSelector.value.replace('station', '');
            const endStation = bikeStations.find(station => station.number == endStationNumber);
          
            if (startStation && endStation) {
              const request = {
                origin: { lat: startStation.position_lat, lng: startStation.position_lng },
                destination: { lat: endStation.position_lat, lng: endStation.position_lng },
                travelMode: 'BICYCLING'
              };
          
              directionsService.route(request, function(result, status) {
                if (status == 'OK') {
                  directionsRenderer.setDirections(result);
                }
              });
            }
          });
      }
      bikeStations = await fetchDublinBikesData();
      availabilityActual= await fetchAvailabilityBikesData();
      createMarkers(map, bikeStations,availabilityActual);

        populateDropdown('#startSelector select', bikeStations);
        populateDropdown('#destinationSelector select', bikeStations);
        
        const locationCheckBox = document.getElementById('locationCheckBox');
  if (locationCheckBox) {
    locationCheckBox.addEventListener('change', async function() {
      if (this.checked) {
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(async function(position) {
            const userLocation = {
              lat: position.coords.latitude,
              lng: position.coords.longitude
            };
            map.setCenter(userLocation);

            const stationsWithBikes = availabilityActual.filter(station => station.available_bikes > 2);            
            const closestStation = stationsWithBikes.reduce((prev, curr) => {
              const d1 = google.maps.geometry.spherical.computeDistanceBetween(
                new google.maps.LatLng(userLocation), 
                new google.maps.LatLng({ lat: prev.lat, lng: prev.lng })
              );
              const d2 = google.maps.geometry.spherical.computeDistanceBetween(
                new google.maps.LatLng(userLocation), 
                new google.maps.LatLng({ lat: curr.lat, lng: curr.lng })
              );
              return d1 < d2 ? prev : curr;
            });

            // Set the starting point to the closest station
            let startStationNumber = closestStation.number;
            for (let station of bikeStations) {
              if (station.number === startStationNumber) {
                const startSelector = document.querySelector('#startSelector select');
                startSelector.value = `station${station.number}`;
                break;
              }
            }

          }, function() {
            handleLocationError(true, infoWindow, map.getCenter());
          });
        } else {
          // Browser doesn't support Geolocation
          handleLocationError(false, infoWindow, map.getCenter());
        }
      }
    });
  }

  } catch (error) {
      console.error('Error importing marker library:', error);
  }
}
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

//function to update the markers every 5 mins
//Does not worki right now. Could be implemented in the future
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
  const seconds= String(today.getSeconds()).padStart(2, '0');
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('dateInput').value = getCurrentDateTime();
})

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
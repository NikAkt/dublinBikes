let bikeStations = [];
const markers = [];
let infoWindow;
let availability;
let map;
let globalClosestStation = null;

const createMarkers = (map, bikeStations, availabilityActual) => {
  bikeStations.forEach((station, i) => {
    let markerColor;
    if (availabilityActual[i].available_bikes === 0) {
      markerColor = "red";
    } else if (availabilityActual[i].available_bikes < 5) {
      markerColor = "orange";
    } else if (availabilityActual[i].available_bikes < 10) {
      markerColor = "green";
    } else {
      markerColor = "blue";
    }

    const marker = new google.maps.Marker({
      position: { lat: station.position_lat, lng: station.position_lng },
      map,
      title: station.name,
      icon: {
        path: google.maps.SymbolPath.CIRCLE,
        fillColor: markerColor,
        fillOpacity: 1,
        strokeColor: "#FFFFFF", // Border color
        strokeWeight: 1, // Border width
        scale: 8, // Size of the marker
      },
    });

    marker.addListener("click", () => {
      if (infoWindow) {
        infoWindow.close();
      }
      infoWindow = new google.maps.InfoWindow({
        content: `<div>${station.name}<br>Available Bikes: ${availabilityActual[i].available_bikes}<br>Available Bike Stands: ${availabilityActual[i].available_bike_stands}</div>`,
      });
      infoWindow.open(map, marker);
      const endSelector = document.querySelector("#destinationSelector select");
      endSelector.value = `station${station.number}`;
    });
    markers.push(marker); //adding each marker to markers array so it can be ecorporated in the cluster
  });
  const markerCluster = new markerClusterer.MarkerClusterer({ markers, map }); //creating the cluster from markers
};

async function initMap() {
  //setting the default display location of the map
  const mapDiv = document.getElementById("map");
  const mapCenter = { lat: 53.3483031, lng: -6.2637067 };

  try {
    if (mapDiv) {
      map = new google.maps.Map(mapDiv, {
        center: mapCenter,
        zoom: 13,
        styles: [
          {
            featureType: "poi",
            stylers: [{ visibility: "off" }],
          },
          {
            featureType: "transit",
            stylers: [{ visibility: "off" }],
          },
          {
            featureType: "all",
            stylers: [{ saturation: -30 }],
          },
        ],
        streetViewControl: false,
      });

      const directionsService = new google.maps.DirectionsService();
      const directionsRenderer = new google.maps.DirectionsRenderer({
        polylineOptions: {
          strokeColor: "magenta",
        },
      });
      directionsRenderer.setMap(map);

      const startSelector = document.querySelector("#startSelector select");

      const endSelector = document.querySelector("#destinationSelector select");
      const goButton = document.getElementById("goButton");

      goButton.addEventListener("click", function () {
        const statsLabel = document.getElementById("statsLabel");

        let isHighlighted = false;
        const blinkInterval = setInterval(() => {
          if (isHighlighted) {
            statsLabel.style.backgroundColor = "";
          } else {
            statsLabel.style.backgroundColor = "#ffffcc";
          }
          isHighlighted = !isHighlighted;
        }, 100); // Blink every 100 milliseconds

        setTimeout(() => {
          clearInterval(blinkInterval);
          statsLabel.style.backgroundColor = "#ffffcc";
        }, 1000);
        const startStationNumber = startSelector.value.replace("station", "");
        const startStation = bikeStations.find(
          (station) => station.number == startStationNumber
        );

        const endStationNumber = endSelector.value.replace("station", "");
        const endStation = bikeStations.find(
          (station) => station.number == endStationNumber
        );
        let esn = endStationNumber;
        let ssn = startStationNumber;
        drawBasic(startStationNumber);
        drawBasic2(endStationNumber);
        let dateInputValue = document.getElementById("dateInput").value;
        console.log(dateInputValue);
        fetch("http://13.48.147.216/predict", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            datetime: dateInputValue,
            station_number_start: ssn,
            station_number_end: esn,
          }),
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
          })
          .then((data) => {
            const predictionBikeAvailabilityStart = Math.round(
              data.prediction_bike_availability_start
            );
            const predictionBikeStandsEnd = Math.round(
              data.prediction_bike_stands_end
            );

            // Get the predictionsDiv element
            const predictionsDiv = document.getElementById("predictionsDiv");

            // Update the innerHTML of predictionsDiv
            predictionsDiv.innerHTML = `
    <h1>Predictions</h1>
    <p id="bikePred">Starting station bike availability: ${predictionBikeAvailabilityStart}</p>
    <p id="bikePred">Destination station bike stand availability: ${predictionBikeStandsEnd}</p>
  `;
          })
          .catch((error) => {
            console.error("Error:", error);
            const predictionsDiv = document.getElementById("predictionsDiv");
            predictionsDiv.innerHTML = `<p>Error: ${error.message}</p>`;
          });

        if (startStation && endStation) {
          const request = {
            origin: {
              lat: startStation.position_lat,
              lng: startStation.position_lng,
            },
            destination: {
              lat: endStation.position_lat,
              lng: endStation.position_lng,
            },
            travelMode: "BICYCLING",
          };

          directionsService.route(request, function (result, status) {
            if (status == "OK") {
              directionsRenderer.setDirections(result);
            }
          });
        }
      });
    }

    document.addEventListener("DOMContentLoaded", function () {
      const statsTab = document.getElementById("statsTab");
      const startSelector = document.querySelector("#startSelector select");
      const endSelector = document.querySelector("#destinationSelector select");

      statsTab.addEventListener("click", function () {
        const startStationNumber = startSelector.value.replace("station", "");
        const endStationNumber = endSelector.value.replace("station", "");
        drawBasic(startStationNumber);
        drawBasic2(endStationNumber);
      });
    });

    function drawBasic(stationId) {
      // Load the Visualization API and the corechart package
      google.charts.load("current", { packages: ["corechart"] });

      // Set a callback to run when the Google Visualization API is loaded
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {
        // Make an AJAX request to get the availability data for the station
        var jqxhr = $.getJSON(
          "/availability_by_hour/" + stationId,
          function (data) {
            var availabilityData = data.availability;

            var chartData = [["Hour", "Bikes Available"]];
            for (var i = 0; i < availabilityData.length; i++) {
              // Convert hour values to numbers
              var hour = parseInt(
                availabilityData[i].hour_start.substring(0, 2)
              );
              chartData.push([
                hour,
                parseFloat(availabilityData[i].avg_bikes_available),
              ]);
            }

            var data = google.visualization.arrayToDataTable(chartData);

            // Set chart options
            var options = {
              title: "Bikes Availability By Hour",
              hAxis: {
                title: "Hour of the Day",
              },
              vAxis: {
                title: "Number of Bikes Available",
              },
              legend: { position: "none" },
              width: 300,
            };

            // Instantiate and draw the chart
            var chart = new google.visualization.LineChart(
              document.getElementById("chartsDiv1")
            );
            chart.draw(data, options);
          }
        );
      }
    }

    function drawBasic2(stationId) {
      // Load the Visualization API and the corechart package
      google.charts.load("current", { packages: ["corechart"] });
      google.charts.setOnLoadCallback(drawChart2);

      function drawChart2() {
        // Make an AJAX request to get the availability data for the station
        var jqxhr = $.getJSON("/stands_by_hour/" + stationId, function (data) {
          console.log("Stands Data:", data);
          var availabilityData = data.availability;

          var chartData = [["Hour", " Available"]];
          for (var i = 0; i < availabilityData.length; i++) {
            // Convert hour values to numbers
            var hour = parseInt(availabilityData[i].hour_start.substring(0, 2));
            chartData.push([
              hour,
              parseFloat(availabilityData[i].avg_stands_available),
            ]);
          }
          console.log("Chart Data:", chartData);

          var data = google.visualization.arrayToDataTable(chartData);

          // Set chart options
          var options = {
            title: "Stands Availability By Hour",
            hAxis: {
              title: "Hour of the Day",
            },
            vAxis: {
              title: "Number of Stands Available",
            },
            legend: { position: "none" },
            width: 300,
          };

          // Instantiate and draw the chart
          var chart = new google.visualization.LineChart(
            document.getElementById("chartsDiv2")
          );
          chart.draw(data, options);
        });
      }
    }

    bikeStations = await fetchDublinBikesData();
    availabilityActual = await fetchAvailabilityBikesData();
    createMarkers(map, bikeStations, availabilityActual);

    populateDropdown("#startSelector select", bikeStations);
    populateDropdown("#destinationSelector select", bikeStations);

    const locationCheckBox = document.getElementById("locationCheckBox");
    if (locationCheckBox) {
      locationCheckBox.addEventListener("change", async function () {
        if (this.checked) {
          if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
              async function (position) {
                const userLocation = {
                  lat: position.coords.latitude,
                  lng: position.coords.longitude,
                };
                map.setCenter(userLocation);

                const stationsWithBikes = availabilityActual.filter(
                  (station) => station.available_bikes > 0
                );
                const closestStation = stationsWithBikes.reduce(
                  (prev, curr) => {
                    const d1 =
                      google.maps.geometry.spherical.computeDistanceBetween(
                        new google.maps.LatLng(userLocation),
                        new google.maps.LatLng({ lat: prev.lat, lng: prev.lng })
                      );
                    const d2 =
                      google.maps.geometry.spherical.computeDistanceBetween(
                        new google.maps.LatLng(userLocation),
                        new google.maps.LatLng({ lat: curr.lat, lng: curr.lng })
                      );
                    return d1 < d2 ? prev : curr;
                  }
                );

                // Set the starting point to the closest station
                let startStationNumber = closestStation.number;
                for (let station of bikeStations) {
                  if (station.number === startStationNumber) {
                    const startSelector = document.querySelector(
                      "#startSelector select"
                    );
                    startSelector.value = `station${station.number}`;
                    break;
                  }
                }
              },
              function () {
                handleLocationError(true, infoWindow, map.getCenter());
              }
            );
          } else {
            // Browser doesn't support Geolocation
            handleLocationError(false, infoWindow, map.getCenter());
          }
        }
      });
    }
  } catch (error) {
    console.error("Error importing marker library:", error);
  }
  initializeFindEmptyStationButton(); //initialize the FindEmptyStation button
}
async function fetchDublinBikesData() {
  try {
    const response = await fetch("/stations");
    const data = await response.json();
    stationData = data.station;
    return stationData;
  } catch (error) {
    console.error("Error fetching Dublin Bikes data:", error);
    return null;
  }
}
async function fetchAvailabilityBikesData() {
  try {
    const response = await fetch("/availability");
    const data = await response.json();
    availability = data.availability;
    temp = availability.reverse();
    availabilityActual = temp;
    return availabilityActual;
  } catch (error) {
    console.error("Error fetching availability data:", error);
    return null;
  }
}

//function to update the markers every 5 mins
//Does not worki right now. Could be implemented in the future
async function updateMarkers() {
  const updatedData = await fetchDublinBikesData();
  if (updatedData !== null) {
    bikeStations = updatedData;
    createMarkers(map, bikeStations, availabilityActual);
  } else {
    console.error("Data not found.");
  }
}

// calling the init map function for displaying google map//
document.addEventListener("DOMContentLoaded", function () {
  initMap();
});

// collapsable dropdown for weather info
var weatherButton = document.getElementById("weatherButton");
if (weatherButton) {
  weatherButton.addEventListener("click", function () {
    this.classList.toggle("active");

    //code for changing icon weatherButton.style.backgroundImage = 'url(' + imageUrl + ')';//
    var weatherContent = this.nextElementSibling;
    if (weatherContent.style.display === "block") {
      weatherContent.style.display = "none";
    } else {
      weatherContent.style.display = "block";
    }
  });
}

//get todays date and time
function getCurrentDateTime() {
  const today = new Date();
  const year = today.getFullYear();
  const month = String(today.getMonth() + 1).padStart(2, "0"); // Months are 0-based
  const day = String(today.getDate()).padStart(2, "0");
  const hours = String(today.getHours()).padStart(2, "0");
  const minutes = String(today.getMinutes()).padStart(2, "0");
  const seconds = String(today.getSeconds()).padStart(2, "0");
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("dateInput").value = getCurrentDateTime();
});

//function to populate the dropwdowns with the stations
function populateDropdown(selector, stations) {
  const selectElement = document.querySelector(selector);
  selectElement.innerHTML = `<option value="">Select a Station</option>`;

  stations.forEach((station) => {
    const option = document.createElement("option");
    option.value = `station${station.number}`;
    option.textContent = station.name;
    selectElement.appendChild(option);
  });
}

//openweather buttom and widget
window.myWidgetParam ? window.myWidgetParam : (window.myWidgetParam = []);
window.myWidgetParam.push(
  {
    id: 23,
    cityid: "2964574",
    appid: "43aeecf5b252d71ca98d7f4dd8aaee24",
    units: "metric",
    containerid: "openweathermap-widget-23", // Container ID for the first widget
  },
  {
    id: 21,
    cityid: "2964574",
    appid: "43aeecf5b252d71ca98d7f4dd8aaee24",
    units: "metric",
    containerid: "openweathermap-widget-21", // Container ID for the second widget
  }
);

(function () {
  var script = document.createElement("script");
  script.async = true;
  script.charset = "utf-8";
  script.src =
    "https://openweathermap.org/themes/openweathermap/assets/vendor/owm/js/weather-widget-generator.js";
  var s = document.getElementsByTagName("script")[0];
  s.parentNode.insertBefore(script, s);
})();

// Event listener for the "Find Location" button.
// It gets the user's address input, geocodes it to coordinates, and then centers the map on this location.
document
  .getElementById("findLocationButton")
  .addEventListener("click", async function () {
    const address = document.getElementById("addressInput").value;
    try {
      const location = await geocodeAddress(address);
      map.setCenter(location);
      popupLocationOnMap(location);
    } catch (error) {
      console.error(error);
      alert("Geocoding failed: " + error);
    }
  });

// Function to display a marker at the given location on the map.
function popupLocationOnMap(location) {
  map.setCenter(location);
  const marker = new google.maps.Marker({
    position: location,
    map: map,
  });
}

// Event listener for the "Find Closest Station" button.
// It finds the nearest bike station to the current map center and updates the global closest station.
document.getElementById("geocodeButton").addEventListener("click", function () {
  const mapCenter = map.getCenter();
  const closestStation = findClosestStation(mapCenter.toJSON());
  globalClosestStation = closestStation;
});

// Function to geocode an address string into coordinates using Google Maps Geocoder.
async function geocodeAddress(address) {
  const geocoder = new google.maps.Geocoder();
  return new Promise((resolve, reject) => {
    geocoder.geocode({ address: address }, (results, status) => {
      if (status === "OK") {
        resolve(results[0].geometry.location);
      } else {
        reject(
          "Geocode was not successful for the following reason: " + status
        );
      }
    });
  });
}

// Function to find the closest bike station to a given location.
function findClosestStation(location) {
  const closestStation = bikeStations.reduce((prev, curr) => {
    const d1 = google.maps.geometry.spherical.computeDistanceBetween(
      new google.maps.LatLng(location),
      new google.maps.LatLng({ lat: prev.position_lat, lng: prev.position_lng })
    );
    const d2 = google.maps.geometry.spherical.computeDistanceBetween(
      new google.maps.LatLng(location),
      new google.maps.LatLng({ lat: curr.position_lat, lng: curr.position_lng })
    );
    return d1 < d2 ? prev : curr;
  });

  // get the closest station location
  const closestStationLocation = {
    lat: closestStation.position_lat,
    lng: closestStation.position_lng,
  };
  globalClosestStation = closestStation; // set it as a global var

  // call popupLocationOnMap fun to pop up the closest station location
  popupLocationOnMap(closestStationLocation);
  return closestStation;
}

// Function to set a bike station as either the start or end point in a selector.
function setStationAs(selectorId, station) {
  if (!station) {
    console.error("Error: station is null or undefined");
    alert(
      "Only a station can be set as the start or end station. Please select the closest station to your location using the 'Find Closest Station' button."
    );

    return;
  }
  document.querySelector(selectorId).value = `station${station.number}`;
}

// Event listeners to set the closest station as either the start or end point.
document.getElementById("setAsStart").addEventListener("click", function () {
  setStationAs("#startSelector select", globalClosestStation);
});

document.getElementById("setAsEnd").addEventListener("click", function () {
  setStationAs("#destinationSelector select", globalClosestStation);
});

// Function to convert a Place object to coordinates, used with Google Places Autocomplete.
async function geocodeAddressFromPlace(place) {
  return new Promise((resolve, reject) => {
    if (!place.geometry) {
      reject("No location found for the entered place.");
    } else {
      resolve(place.geometry.location);
    }
  });
}

// Setting up Google Maps Autocomplete for the address input field.
const input = document.getElementById("addressInput");
const options = {
  componentRestrictions: { country: "ie" }, // Restrict results to Ireland using its country code
};
const autocomplete = new google.maps.places.Autocomplete(input, options);

// Listener for when a place is selected in the autocomplete field.
// It geocodes the selected place and updates the map.
autocomplete.addListener("place_changed", function () {
  const place = autocomplete.getPlace();
  if (!place.geometry) {
    console.log("No details available for input: '" + place.name + "'");
    return;
  }
});

// Function to initializes the button for finding empty stations.(It is called in the end of intMap)
function initializeFindEmptyStationButton() {
  const findEmptyStationButton = document.getElementById(
    "findEmptyStationButton"
  );

  findEmptyStationButton.addEventListener("click", function () {
    const mapCenter = map.getCenter();

    const closestStationWithStands = findClosestStationWithAvailableStands(
      mapCenter.toJSON(),
      availabilityActual
    );

    globalClosestStation = closestStationWithStands;
  });
}

// Function to find the closest station with available bike stands.
function findClosestStationWithAvailableStands(location, availabilityActual) {
  let shortestDistance = Infinity;
  let closestStationWithStands = null;

  bikeStations.forEach((station, i) => {
    if (availabilityActual[i].available_bike_stands > 0) {
      const stationLocation = new google.maps.LatLng({
        lat: station.position_lat,
        lng: station.position_lng,
      });

      const distance = google.maps.geometry.spherical.computeDistanceBetween(
        new google.maps.LatLng(location),
        stationLocation
      );

      if (distance < shortestDistance) {
        shortestDistance = distance;
        closestStationWithStands = station;
      }
    }
  });

  // If a closest station with available stands is found.
  if (closestStationWithStands) {
    // Creating an object for the closest station's coordinates.
    const closestStationWithStandsCoords = {
      lat: closestStationWithStands.position_lat,
      lng: closestStationWithStands.position_lng,
    };

    globalclosestStationWithStands = closestStationWithStandsCoords;
    popupLocationOnMap(closestStationWithStandsCoords);
  }
}

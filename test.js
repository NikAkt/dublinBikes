// Function to fetch Dublin Bikes data
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

// Function to format data into JSON
async function formatDataToJson() {
    const dublinBikesData = await fetchDublinBikesData();
    if (dublinBikesData) {
        const jsonData = JSON.stringify(dublinBikesData, null, 2);
        console.log(jsonData);
        return jsonData;
    } else {
        console.log('Failed to fetch data.');
        return null;
    }
}

// Example usage
formatDataToJson()
    .then(jsonData => {
        // You can further process jsonData here
    })
    .catch(error => {
        // Handle any errors
        console.error('Error:', error);
    });

// Function to fetch weather data
async function fetchWeatherData(cityName, apiKey) {
    try {
        const response = await fetch(`https://api.openweathermap.org/data/2.5/weather?q=${cityName}&appid=${apiKey}`);
        const weatherData = await response.json();
        return weatherData;
    } catch (error) {
        console.error('Error fetching weather data:', error);
        return null;
    }
}

// Example usage
const cityName = 'Dublin'; // Replace with the city name you want to fetch data for
const apiKey = '43aeecf5b252d71ca98d7f4dd8aaee24'; // Replace with your OpenWeather API key

fetchWeatherData(cityName, apiKey)
    .then(weatherData => {
        // Handle the data
        console.log(weatherData);
    })
    .catch(error => {
        // Handle any errors
        console.error('Error:', error);
    });

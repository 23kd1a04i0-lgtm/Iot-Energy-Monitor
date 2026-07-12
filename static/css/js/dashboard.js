async function updateSensor() {

    try {

        const response = await fetch("/api/sensor");
        const data = await response.json();

        // Update Dashboard Cards
        document.getElementById("voltage").innerHTML = data.voltage + " V";
        document.getElementById("current").innerHTML = data.current + " A";
        document.getElementById("power").innerHTML = data.power + " W";
        document.getElementById("energy").innerHTML = data.energy + " kWh";
        document.getElementById("cost").innerHTML = "₹ " + data.cost;

        // High Power Alert
        if (data.power > 500) {
            document.getElementById("powerAlert").style.display = "block";
        } else {
            document.getElementById("powerAlert").style.display = "none";
        }

        // Update Chart
        energyChart.data.labels.push(data.time);
        energyChart.data.datasets[0].data.push(data.energy);

        // Keep only last 10 readings
        if (energyChart.data.labels.length > 10) {
            energyChart.data.labels.shift();
            energyChart.data.datasets[0].data.shift();
        }

        energyChart.update();

    } catch (error) {
        console.log(error);
    }
}

// Run immediately
updateSensor();

// Update every 3 seconds
setInterval(updateSensor, 3000);


function toggleDarkMode(){

    document.body.classList.toggle("dark-mode");

}
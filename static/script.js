const socket = io();
const devicesDiv = document.getElementById("devices");
devicesDiv.classList.add("justify-content-center");

// Tracks devices by id
const deviceMap = {};

// Maps device status
const statusColors = {
  ACTIVE: "bg-success",
  ISOLATED: "bg-secondary",
};

/* 
  Receives real-time update from the backend (Flask & MQTT smart gateway)
  and updates and creates cards for each device
*/
socket.on("update", (msg) => {
  console.log("Data received: ", msg);

  // Asigns device to a column
  let col = deviceMap[msg.device];
  const statusClass = statusColors[msg.status] || "bg-dark"; // Assigns color to status

  // Creates a column to put cards into
  if (!col) {
    col = document.createElement("div");
    col.className = "col-12 col-md-4";

    devicesDiv.appendChild(col);
    deviceMap[msg.device] = col;
  }

  // Updates the device card inside the column
  col.innerHTML = `
      <div class="card px-4">
        <h3 class="card-title my-2">${msg.device}</h3>
        <p class="card-text">Temperature: ${msg.temperature} °C</p>
        <span class="badge ${statusClass} p-2 mb-3">${msg.status}</span>
      </div>
    `;
});

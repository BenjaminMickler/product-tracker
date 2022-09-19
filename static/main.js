let socket = new WebSocket("ws://producttracker.benmickler.com:8765/");

socket.onopen = function(e) {
    console.log("[open] Connection established");
    console.log("Sending request for all product data");
    socket.send("REQUEST ALL PRODUCT DATA");
};

socket.onmessage = function(event) {
    if (event.data.includes("ALL PRODUCT DATA")) {
        console.log("Received all product data");
        let products = JSON.parse(event.data.split("ALL PRODUCT DATA")[1]);
        let table = document.createElement("table");
        let header = document.createElement("tr");
        let nameHeader = document.createElement("th");
        nameHeader.innerHTML = "Name";
        let priceHeader = document.createElement("th");
        priceHeader.innerHTML = "Price";
        header.appendChild(nameHeader);
        header.appendChild(priceHeader);
        table.appendChild(header);
        for (let i = 0; i < products.length; i++) {
            let row = document.createElement("tr");
            let name = document.createElement("td");
            name.innerHTML = products[i].name;
            let price = document.createElement("td");
            price.innerHTML = products[i].price;
            row.appendChild(name);
            row.appendChild(price);
            table.appendChild(row);
        }
        document.body.appendChild(table);
    }
};

socket.onclose = function(event) {
  if (event.wasClean) {
    alert(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
  } else {
    // e.g. server process killed or network down
    // event.code is usually 1006 in this case
    alert('[close] Connection died');
  }
};

socket.onerror = function(error) {
  alert(`[error] ${error.message}`);
};
let socket = new WebSocket("ws://producttracker.benmickler.com:8765/");

// create event handler for buttons
function createEventHandler() {
    let buttons = document.querySelectorAll("button");
    for (let i = 0; i < buttons.length; i++) {
        buttons[i].addEventListener("click", function() {
            let id = this.getAttribute("id");
            if (id == "add") {
                socket.send("add");
            }
            else if (id == "remove") {
                // get currently selected product
                let selected = document.querySelector("input[name='product']:checked");
                if (selected != null) {
                    socket.send("DELETE " + selected.value);
                }
            }
        });
    }
}

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
        // create selectable rows for each product
        for (let i = 0; i < products.length; i++) {
            let row = document.createElement("tr");
            let name = document.createElement("td");
            name.innerHTML = products[i].name;
            let price = document.createElement("td");
            price.innerHTML = products[i].price;
            let radio = document.createElement("input");
            radio.setAttribute("type", "radio");
            radio.setAttribute("name", "product");
            radio.setAttribute("value", products[i].name);
            row.appendChild(radio);
            row.appendChild(name);
            row.appendChild(price);
            table.appendChild(row);
        }
        document.querySelector("#products").appendChild(table);
        createEventHandler();
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
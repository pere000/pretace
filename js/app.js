function loadText() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "data/example.txt", true);

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            document.getElementById("output").textContent = xhr.responseText;
        }
    };

    xhr.send(null);
}

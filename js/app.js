function loadText(filename) {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "data/" + filename + "?t=" + new Date().getTime(), true);

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            // Render HTML instead of plain text
            document.getElementById("output").innerHTML = xhr.responseText;
        }
    };

    xhr.send(null);
}

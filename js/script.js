document.querySelectorAll('a[href]').forEach(a => {
    a.setAttribute('target', '_blank');

    const icon = document.createElement('span');
    icon.textContent = '⏩️';
    icon.style.fontSize = '18px';
    icon.style.fontStyle = 'normal';

    a.prepend(icon);
});

function loadTmp() {
    fetch("./tmp.txt?cache=" + Date.now())
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.text();
        })
        .then(text => {
            document.getElementById("tmp").innerHTML = text;
        })
        .catch(error => {
            document.getElementById("tmp").innerHTML =
                "<p style='color:red;'>Error loading tmp.txt</p>";
            console.error("Error loading tmp.txt:", error);
        });
}

document.getElementById("loadBtn").addEventListener("click", () => {
    // Create a hidden file input dynamically
    const input = document.createElement("input");
    input.type = "file";

    input.onchange = () => {
        if (input.files.length === 0) return;

        const file = input.files[0];
        const reader = new FileReader();

        reader.onload = (e) => {
            document.getElementById("tmap").innerHTML = e.target.result;
        };

        reader.readAsText(file);
    };

    // Trigger the file picker
    input.click();
});

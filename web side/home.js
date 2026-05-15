const input = document.getElementById("imageInput");
const preview = document.getElementById("preview");
const result = document.getElementById("result");
const loader = document.getElementById("loader");
const btn = document.getElementById("predictBtn");

// Show preview
input.addEventListener("change", () => {
  const file = input.files[0];
  if (file) {
      preview.src = URL.createObjectURL(file);
      preview.style.display = "block";
  }
});

// Send to FastAPI
btn.addEventListener("click", async () => {
  const file = input.files[0];
  if (!file) {
    alert("Please upload an image first.");
    return;
}

const formData = new FormData();
formData.append("file", file);

loader.classList.remove("hidden");
result.innerText = "Predicting...";

// const div = document.createElement('div')
try {
    const response = await fetch("http://127.0.0.1:9000/predict", {
        method: "POST",
        body: formData
    });

    const data = await response.json();
    const predictedClass = data['predicted']
    const confidence = data['confidence']

    result.innerText = `Predicted: ${predictedClass} (${confidence}%)`;
} catch (error) {
    result.innerText = "Error connecting to server.";
}
loader.classList.add("hidden");
});

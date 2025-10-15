function ask() {
  const prompt = document.getElementById("prompt").value;
  const responseDiv = document.getElementById("response");
  responseDiv.innerText = "Loading...";

  fetch("/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ prompt: prompt })
  })
  .then(res => res.json())
  .then(data => {
    responseDiv.innerText = data.response;
  })
  .catch(() => {
    responseDiv.innerText = "Error. Try again.";
  });
}

document.getElementById("resumeForm").addEventListener("submit", function(e) {
  e.preventDefault();
  const formData = new FormData();
  const fileInput = document.getElementById("resume");
  const uploadStatus = document.getElementById("uploadStatus");

  formData.append("resume", fileInput.files[0]);
  uploadStatus.innerText = "Uploading...";

  fetch("/upload_resume", {
    method: "POST",
    body: formData
  })
  .then(res => res.json())
  .then(data => {
    uploadStatus.innerText = data.status;
  })
  .catch(() => {
    uploadStatus.innerText = "Upload failed.";
  });
});
document.getElementById("patientForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const patientData = {
        name: document.getElementById("name").value,
        age: parseInt(document.getElementById("age").value),
        gender: document.getElementById("gender").value,
        bloodgroup: document.getElementById("bloodgroup").value,
        mobile: document.getElementById("mobile").value,
        address: document.getElementById("address").value
    };

    const response = await fetch("http://localhost:8000/patients", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(patientData)
    });

    const data = await response.json();

    // Save patient_id for upload page
    localStorage.setItem("patient_id", data.patient_id);

    // Redirect to upload page
    window.location.href = "upload.html";
});
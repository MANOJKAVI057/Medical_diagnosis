const API = "http://127.0.0.1:8000";
const token = localStorage.getItem("token");
const user = localStorage.getItem("user");

/* ================= AUTH CHECK ================= */
if (!token) {
    window.location.href = "login.html";
}

/* ================= SET DOCTOR NAME ================= */
document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("doctorName").innerText =
        user || "Doctor";

    loadAnalytics();
    loadPatients();
});

/* ================= NAVIGATION ================= */
function goUpload() { window.location.href = "upload.html"; }
function goabout() { window.location.href = "about.html"; }
function gosetting() { window.location.href = "setting.html"; }
function gopatient_history() { window.location.href = "patient_history.html"; }
function gonew_patient() { window.location.href = "patient-info.html"; }
function gorules() { window.location.href = "rule.html"; }

function logout() {
    localStorage.clear();
    window.location.href = "login.html";
}

/* ================= ANALYTICS ================= */
let myChart;

async function loadAnalytics() {
    try {
        const res = await fetch(`${API}/analytics`, {
            headers: { Authorization: "Bearer " + token }
        });

        if (res.status === 401) {
            alert("Session expired. Login again.");
            window.location.href = "login.html";
            return;
        }

        const data = await res.json();
        console.log("Analytics data:", data);

        const distribution = data.diagnosis_distribution;

        const labels = Object.keys(distribution);
        const values = Object.values(distribution);

        if (myChart) myChart.destroy();

        myChart = new Chart(document.getElementById("chart"), {
            type: "bar",
            data: {
                labels: labels,
                datasets: [{
                    label: "Diagnosis Cases",
                    data: values,
                    backgroundColor: "rgba(0,198,255,0.8)"
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });

    } catch (err) {
        console.log("Analytics error:", err);
    }
}

/* ================= PATIENT LIST ================= */
async function loadPatients() {
    try {
        const response = await fetch(`${API}/patients`, {
            headers: { Authorization: "Bearer " + token }
        });

        const patients = await response.json();
        const container = document.getElementById("patientList");
        container.innerHTML = "";

        patients.forEach(patient => {
            const div = document.createElement("div");
            div.innerHTML = `
                <p>
                    <strong>${patient.name}</strong> (Age: ${patient.age})
                    <button onclick="viewPatient('${patient._id}')">View</button>
                </p>
            `;
            container.appendChild(div);
        });

    } catch (err) {
        console.log("Patient load error:", err);
    }
}

function viewPatient(id) {
    window.location.href = `patient-profile.html?id=${id}`;
}

/* ================= THEME ================= */
function toggleTheme() {
    const current = document.documentElement.getAttribute("data-theme");
    const newTheme = current === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", newTheme);
    localStorage.setItem("theme", newTheme);
}

/* Load saved theme */
const savedTheme = localStorage.getItem("theme") || "dark";
document.documentElement.setAttribute("data-theme", savedTheme);
document.getElementById("diagnosisForm").onsubmit = async(e)=>{
    e.preventDefault();

    let formData = new FormData();
    formData.append("patientname",patientname.value);
    formData.append("age",age.value);
    formData.append("heart_rate",hr.value);
    formData.append("systolic_bp",bp1.value);
    formData.append("diastolic_bp",bp2.value);
    formData.append("spo2",spo2.value);
    formData.append("temperature",temp.value);
    formData.append("image",image.files[0]);

    const res = await fetch(API + "/diagnose/", {
    method: "POST",
    headers: {
        "Authorization": "Bearer " + token
    },
    body: formData
});

    const data = await res.json();
    document.getElementById("result").innerHTML =
        `<h2>Diagnosis: ${data.diagnosis}</h2>`;
};
// Show selected section

function showSection(sectionId) {

    const sections = document.querySelectorAll(".section");

    sections.forEach(function(section) {
        section.classList.add("hidden");
    });

    document.getElementById(sectionId).classList.remove("hidden");
}


// Student Form

document.getElementById("studentForm").addEventListener("submit", function(event) {

    event.preventDefault();

    const name = document.getElementById("studentName").value;
    const email = document.getElementById("studentEmail").value;
    const department = document.getElementById("department").value;
    const cgpa = parseFloat(document.getElementById("cgpa").value);
    const graduationYear = parseInt(
        document.getElementById("graduationYear").value
    );
    const skills = document.getElementById("skills").value;


    // Validate CGPA

    if (cgpa < 5 || cgpa > 10) {
        alert("CGPA must be between 5 and 10.");
        return;
    }


    // Validate Graduation Year

    if (graduationYear < 2020) {
        alert("Graduation year must be 2020 or later.");
        return;
    }


    const studentList = document.getElementById("studentList");

    const student = document.createElement("div");

    student.className = "list-item";

    student.innerHTML = `
        <strong>${name}</strong><br>
        Email: ${email}<br>
        Department: ${department}<br>
        CGPA: ${cgpa}<br>
        Graduation Year: ${graduationYear}<br>
        Skills: ${skills}
    `;

    studentList.appendChild(student);

    document.getElementById("studentForm").reset();

    updateCounts();
});


// Company Form

document.getElementById("companyForm").addEventListener("submit", function(event) {

    event.preventDefault();

    const name = document.getElementById("companyName").value;
    const location = document.getElementById("location").value;
    const industry = document.getElementById("industry").value;
    const website = document.getElementById("website").value;

    const companyList = document.getElementById("companyList");

    const company = document.createElement("div");

    company.className = "list-item";

    company.innerHTML = `
        <strong>${name}</strong><br>
        Location: ${location}<br>
        Industry: ${industry}<br>
        Website: ${website}
    `;

    companyList.appendChild(company);

    document.getElementById("companyForm").reset();

    updateCounts();
});


// Job Form

document.getElementById("jobForm").addEventListener("submit", function(event) {

    event.preventDefault();

    const companyId = document.getElementById("companyId").value;
    const jobTitle = document.getElementById("jobTitle").value;
    const packageValue = document.getElementById("package").value;
    const eligibility = document.getElementById("eligibility").value;
    const deadline = document.getElementById("deadline").value;

    const jobList = document.getElementById("jobList");

    const job = document.createElement("div");

    job.className = "list-item";

    job.innerHTML = `
        <strong>${jobTitle}</strong><br>
        Company ID: ${companyId}<br>
        Package: ${packageValue} LPA<br>
        Eligibility: ${eligibility}<br>
        Deadline: ${deadline}
    `;

    jobList.appendChild(job);

    document.getElementById("jobForm").reset();

    updateCounts();
});


// Application Form

document.getElementById("applicationForm").addEventListener("submit", function(event) {

    event.preventDefault();

    const studentId =
        document.getElementById("applicationStudentId").value;

    const jobId =
        document.getElementById("applicationJobId").value;

    const applicationDate =
        document.getElementById("applicationDate").value;

    const status =
        document.getElementById("applicationStatus").value;


    const applicationList =
        document.getElementById("applicationList");

    const application = document.createElement("div");

    application.className = "list-item";

    application.innerHTML = `
        Student ID: ${studentId}<br>
        Job ID: ${jobId}<br>
        Application Date: ${applicationDate}<br>
        Status: ${status}
    `;

    applicationList.appendChild(application);

    document.getElementById("applicationForm").reset();

    updateCounts();
});


// Update Dashboard Counts

function updateCounts() {

    const students =
        document.querySelectorAll("#studentList .list-item").length;

    const companies =
        document.querySelectorAll("#companyList .list-item").length;

    const jobs =
        document.querySelectorAll("#jobList .list-item").length;

    const applications =
        document.querySelectorAll("#applicationList .list-item").length;


    document.getElementById("studentCount").textContent = students;

    document.getElementById("companyCount").textContent = companies;

    document.getElementById("jobCount").textContent = jobs;

    document.getElementById("applicationCount").textContent = applications;
}


// Show Home section when page loads

showSection("home");
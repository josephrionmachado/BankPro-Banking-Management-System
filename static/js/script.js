
/* =========================================
   BANKPRO - DASHBOARD JAVASCRIPT
========================================= */


// =========================================
// SIDEBAR TOGGLE
// =========================================

const menuToggle = document.getElementById("menuToggle");
const sidebar = document.getElementById("sidebar");

if (menuToggle && sidebar) {
    menuToggle.addEventListener("click", function () {
        sidebar.classList.toggle("active");
    });
}


// =========================================
// CURRENT DATE DISPLAY
// =========================================

function displayCurrentDate() {

    const today = new Date();

    const options = {
        weekday: "long",
        year: "numeric",
        month: "long",
        day: "numeric"
    };

    const formattedDate = today.toLocaleDateString("en-IN", options);

    const topbarDate = document.getElementById("currentDate");
    const dashboardDate = document.getElementById("dashboardDate");

    if (topbarDate) {
        topbarDate.textContent = formattedDate;
    }

    if (dashboardDate) {
        dashboardDate.textContent = formattedDate;
    }
}

displayCurrentDate();


// =========================================
// CLOSE SIDEBAR AFTER NAVIGATION
// ON MOBILE DEVICES
// =========================================

const navigationLinks = document.querySelectorAll(".sidebar .nav-link");

navigationLinks.forEach(function (link) {

    link.addEventListener("click", function () {

        if (window.innerWidth <= 768 && sidebar) {
            sidebar.classList.remove("active");
        }

    });

});


// =========================================
// CURRENT YEAR
// =========================================

const footer = document.querySelector(".sidebar-footer");

if (footer) {
    const yearText = footer.querySelector("span");

    if (yearText) {
        yearText.textContent = `BankPro © ${new Date().getFullYear()}`;
    }
}


// =========================================
// NUMBER CARD ANIMATION
// =========================================

const statisticNumbers = document.querySelectorAll(".stat-info h2");

statisticNumbers.forEach(function (element) {

    element.style.transition = "opacity 0.5s ease";

    element.style.opacity = "0";

    setTimeout(function () {
        element.style.opacity = "1";
    }, 150);

});


// =========================================
// RESPONSIVE SIDEBAR
// =========================================

window.addEventListener("resize", function () {

    if (window.innerWidth > 768 && sidebar) {
        sidebar.classList.remove("active");
    }

});

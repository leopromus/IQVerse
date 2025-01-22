document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.getElementById("sidebar");
    const menuToggle = document.getElementById("menuToggle"); // Menu button to open sidebar
    const sidebarToggle = document.getElementById("sidebarToggle"); // Button to close/minimize sidebar
    const links = document.querySelectorAll(".sidebar-menu li a"); // Navigation links
    const sections = document.querySelectorAll(".content-section"); // Content sections

    // Toggle sidebar on menu button click (open/close)
    menuToggle.addEventListener("click", () => {
        sidebar.classList.toggle("active"); // Show/hide sidebar
    });

    // Close/minimize sidebar on close button click
    sidebarToggle.addEventListener("click", () => {
        sidebar.classList.toggle("minimized"); // Add/remove minimized class

        // Change the text/icon of the close button based on state
        if (sidebar.classList.contains("minimized")) {
            sidebarToggle.textContent = "Expand"; // Change text/icon to 'Expand'
        } else {
            sidebarToggle.textContent = "Minimize"; // Change text/icon to 'Minimize'
        }
    });

    // Navigation links functionality
    links.forEach(link => {
        link.addEventListener("click", (e) => {
            e.preventDefault(); // Prevent default link behavior

            // Remove 'active' class from all links and add it to the clicked link
            links.forEach(l => l.classList.remove("active"));
            link.classList.add("active");

            // Show the corresponding content section
            const target = link.getAttribute("data-target");
            sections.forEach(section => {
                section.classList.remove("active");
                if (section.id === target) {
                    section.classList.add("active");
                }
            });
        });
    });
});

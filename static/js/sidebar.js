
const sidebarSubMenus = document.querySelectorAll('.sub-menu');
const sidebarSubMenuToggleDropdowns = document.querySelectorAll('.ti-angle-down');


const path = window.location.pathname;
const page = path.split("/").pop();


if (page === "_create-product.html" || page === "_manage-product.html") {
    sidebarSubMenus[0].style.display = "block";
    for (i = 0; i < sidebarSubMenuToggleDropdowns.length; i++) {
        sidebarSubMenuToggleDropdowns[i].addEventListener("click", function () {
            this.classList.toggle("active");
            const dropdownContent = this.parentElement.parentElement.nextElementSibling;

            if (dropdownContent.style.display === "block") {
                sidebarSubMenus.forEach(subMenu => {
                    subMenu.style.display = "none";
                });
                dropdownContent.style.display = "none";
            } else {
                sidebarSubMenus.forEach(subMenu => {
                    subMenu.style.display = "none";
                });
                dropdownContent.style.display = "block";
            }
        });
    }
} else {
    for (i = 0; i < sidebarSubMenuToggleDropdowns.length; i++) {
        sidebarSubMenuToggleDropdowns[i].addEventListener("click", function () {
            this.classList.toggle("active");
            const dropdownContent = this.parentElement.parentElement.nextElementSibling;

            if (dropdownContent.style.display === "block") {
                sidebarSubMenus.forEach(subMenu => {
                    subMenu.style.display = "none";
                });
                dropdownContent.style.display = "none";
            } else {
                sidebarSubMenus.forEach(subMenu => {
                    subMenu.style.display = "none";
                });
                dropdownContent.style.display = "block";
            }
        });
    }
}




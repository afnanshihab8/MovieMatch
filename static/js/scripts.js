function toggleSection(id) {
    let section = document.getElementById(id);
    if (section.style.display === "none") {
        section.style.display = "block";
    } else {
        section.style.display = "none";
    }
}

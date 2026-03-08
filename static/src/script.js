import { getDestinations } from "./api-functions.js";
console.log("Script loaded");
window.addEventListener("load", async () => {
    const destinations = await getDestinations();
    if (!destinations)
        return;
    const container = document.getElementById("destinationsContainer");
    destinations.forEach((dest) => {
        const p = document.createElement("p");
        p.textContent = dest.title;
        container?.appendChild(p);
    });
});
const h1 = document.getElementById("h1");
h1.addEventListener("mouseover", () => {
    console.log("Hej hej hej");
});
//# sourceMappingURL=script.js.map
import { getDestinations } from "./api-functions.js";

// Henter destinationer
window.addEventListener("load", async () => {
  const destinations = await getDestinations();

  destinations.map((destination) => {
    const template: any = document.getElementById("destinationCardTemplate");
    const kopi: any = template.content.cloneNode(true);

    kopi.getElementById("title").textContent = destination.destination_title;
    kopi.getElementById("description").textContent = destination.destination_description;
    kopi.getElementById("destination").textContent = destination.destination_country + ", " + destination.destination_location;
    kopi.getElementById("date").textContent = destination.destination_date_from + "-" + destination.destination_date_to;

    document.getElementById("destinationsContainer").appendChild(kopi);
  });
});

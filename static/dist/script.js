import { getDestinations } from "./api-functions.js";
// Henter destinationer
window.addEventListener("load", async () => {
    const destinations = await getDestinations();
    destinations.map((destination) => {
        const template = document.getElementById("destinationCardTemplate");
        const kopi = template.content.cloneNode(true);
        kopi.getElementById("title").textContent = destination.destination_title;
        kopi.getElementById("description").textContent = destination.destination_description;
        kopi.getElementById("destination").textContent = destination.destination_country + ", " + destination.destination_location;
        kopi.getElementById("date").textContent = destination.destination_date_from + "-" + destination.destination_date_to;
        // Tilføj delete funktion til KUN ejeren (kun ejeren kan se knappen)
        const deleteBtn = kopi.querySelector(".deleteBtn");
        if (!destination.is_owner && deleteBtn) {
            deleteBtn.remove();
        }
        else if (deleteBtn) {
            deleteBtn.addEventListener("click", async () => {
                const shouldDelete = await showCustomConfirm(`Er du sikker på, at du vil slette "${destination.destination_title}"?`);
                if (!shouldDelete)
                    return;
                try {
                    const response = await fetch(`/api/destinations/${destination.destination_pk}`, { method: "DELETE" });
                    if (response.status === 204) {
                        deleteBtn.closest(".destination").remove();
                    }
                    else {
                        alert("Kunne ikke slette destinationen");
                    }
                }
                catch (error) {
                    console.error("Fejl ved sletning:", error);
                    alert("Der opstod en fejl under sletning");
                }
            });
        }
        // Tilføj edit funktion til KUN ejeren (kun ejeren kan se linket)
        const editLink = kopi.querySelector(".editLink");
        if (!destination.is_owner && editLink) {
            editLink.remove();
        }
        else if (editLink) {
            editLink.href = `/edit-destination/${destination.destination_pk}`;
        }
        document.getElementById("destinationsContainer").appendChild(kopi);
    });
});
// Bekræftelses-dialog funktion
function showCustomConfirm(message) {
    return new Promise((resolve) => {
        const overlay = document.getElementById("customConfirm");
        const messageEl = document.getElementById("customConfirmMessage");
        const yesBtn = document.getElementById("confirmYes");
        const noBtn = document.getElementById("confirmNo");
        messageEl.textContent = message;
        overlay.classList.remove("hidden");
        const cleanUp = () => {
            overlay.classList.add("hidden");
            yesBtn.removeEventListener("click", onYes);
            noBtn.removeEventListener("click", onNo);
        };
        const onYes = () => {
            cleanUp();
            resolve(true);
        };
        const onNo = () => {
            cleanUp();
            resolve(false);
        };
        yesBtn.addEventListener("click", onYes);
        noBtn.addEventListener("click", onNo);
    });
}
//# sourceMappingURL=script.js.map
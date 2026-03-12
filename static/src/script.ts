import { getDestinations } from "./api-functions.js";

// Henter destinationer
window.addEventListener("load", async () => {
  const destinations = await getDestinations();

  destinations.forEach((destination) => {
    const template: any = document.getElementById("destinationCardTemplate");
    const kopi: any = template.content.cloneNode(true);

    kopi.getElementById("title").textContent = destination.destination_title;
    kopi.getElementById("description").textContent = destination.destination_description;
    kopi.getElementById("destination").textContent = destination.destination_country + ", " + destination.destination_location;
    kopi.getElementById("date").textContent = destination.destination_date_from_formatted + " to " + destination.destination_date_to_formatted;

    // Tilføj delete funktion til KUN ejeren (kun ejeren kan se knappen)
    const deleteBtn = kopi.querySelector(".deleteBtn") as HTMLButtonElement;

    if (!destination.is_owner && deleteBtn) {
      deleteBtn.remove();
    } else if (deleteBtn) {
      deleteBtn.addEventListener("click", async (e) => {
        e.preventDefault();
        const shouldDelete = await showCustomConfirm(`Er du sikker på, at du vil slette "${destination.destination_title}"?`);
        if (!shouldDelete) return;

        try {
          const response = await fetch(`/api/destinations/${destination.destination_pk}`, {
            method: "DELETE",
            credentials: "same-origin",
          });
          console.log("Fetch status:", response.status);
          const text = await response.text();
          console.log("Response text:", text);

          if (response.status === 204) {
            const destinationElement = deleteBtn.closest(".destinationCard") as HTMLElement;
            if (destinationElement) {
              destinationElement.remove();
            } else {
              alert(`Kunne ikke slette destinationen: ${response.status} - ${text}`);
              console.warn("Kunne ikke finde destinationCard til fjernelse");
            }
          } else {
            const text = await response.text();
            console.log("Response text:", text);
            alert("Kunne ikke slette destinationen");
          }
        } catch (error) {
          console.error("Fejl ved sletning:", error);
          alert("Der opstod en fejl under sletning");
        }
      });
    }

    // Tilføj edit funktion til KUN ejeren (kun ejeren kan se linket)
    const editBtn = kopi.querySelector(".editBtn") as HTMLAnchorElement;
    if (!destination.is_owner && editBtn) {
      editBtn.remove();
    } else if (editBtn) {
      editBtn.href = `/edit-destination/${destination.destination_pk}`;
    }

    document.getElementById("destinationsContainer").appendChild(kopi);
  });
});

document.addEventListener("submit", (e) => {
  const form = e.target as HTMLFormElement;
  const dateFrom = form.querySelector<HTMLInputElement>('input[name="date_from"]');
  const dateTo = form.querySelector<HTMLInputElement>('input[name="date_to"]');
  if (!dateFrom || !dateTo) return;

  dateFrom.classList.remove("input-error");
  dateTo.classList.remove("input-error");

  const fromVal = dateFrom.value;
  const toVal = dateTo.value;

  let valid = true;

  // check required
  if (!fromVal || !toVal) valid = false;

  // check start < slut
  if (fromVal && toVal && new Date(fromVal) > new Date(toVal)) valid = false;

  if (!valid) {
    dateFrom.classList.add("input-error");
    dateTo.classList.add("input-error");
    e.preventDefault(); // afbryd submit
  }
});

// Bekræftelses-dialog funktion
function showCustomConfirm(message: string): Promise<boolean> {
  return new Promise((resolve) => {
    const overlay = document.getElementById("customConfirm") as HTMLElement;
    const messageEl = document.getElementById("customConfirmMessage") as HTMLElement;
    const yesBtn = document.getElementById("confirmYes") as HTMLButtonElement;
    const noBtn = document.getElementById("confirmNo") as HTMLButtonElement;

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

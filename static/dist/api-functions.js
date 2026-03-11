export async function getDestinations() {
    let url = "/api/destinations";
    // hvis vi er på profile siden
    if (window.location.pathname === "/profile") {
        url = "/api/profile";
    }
    const response = await fetch(url);
    return await response.json();
}
//# sourceMappingURL=api-functions.js.map
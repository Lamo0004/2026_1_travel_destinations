// Henter destinationer
export async function getDestinations() {
    try {
        const response = await fetch("/api/destinations"); // relativ sti
        if (!response.ok)
            return [];
        return await response.json();
    }
    catch (error) {
        console.error("Fejl i fetch:", error);
        return [];
    }
}
//# sourceMappingURL=api-functions.js.map
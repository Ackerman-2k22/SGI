document.addEventListener('DOMContentLoaded', function() {
    const filterForm = document.getElementById('filter-form');
    if (filterForm) {
        filterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const url = "/filter-incidents"; // Assurez-vous que cette URL correspond à votre configuration de backend
            const formData = new FormData(filterForm);

            const tableOutput = document.querySelector(".table-output");
            const appTable = document.querySelector(".app-table");
            const paginationContainer = document.querySelector(".pagination-container");
            const noResults = document.querySelector(".no-results");
            const tbody = document.querySelector(".table-output .table-body");

            // Masquer la table principale et la pagination, afficher la table de sortie
            if (appTable) appTable.style.display = "none";
            if (paginationContainer) paginationContainer.style.display = "none";
            if (tableOutput) tableOutput.style.display = "block";
            if (tbody) tbody.innerHTML = ""; // Vider le tableau actuel

            fetch(url + '?' + new URLSearchParams(formData).toString(), {
                method: 'GET',
            })
            .then(response => response.json())
            .then(data => {
                console.log("Réponse reçue:", data);
                if (Array.isArray(data)) {
                    if (data.length === 0) {
                        if (noResults) noResults.style.display = "block";
                    } else {
                        if (noResults) noResults.style.display = "none";
                        data.forEach(item => {
                            const row = `
                                <tr>
                                    <td>${item.id}</td>
                                    <td>${item.client__username}</td>
                                    <td>${item.description}</td>
                                    <td>${item.category}</td>
                                    <td>${item.created_at}</td>
                                    <td>${item.status}</td>
                                    <td>${item.assigned_agent ? item.assigned_agent : 'Non attribué'}</td>
                                    <td>${item.comment ? item.comment : 'Non spécifié'}</td>
                                    <td>${item.resolved_at}</td>
                                    <td><a href="/edit-incidents/${item.id}" class="btn btn-secondary btn-sm">Edit</a></td>
                                </tr>
                            `;
                            tbody.innerHTML += row;
                        });
                    }
                } else {
                    console.error('La réponse n\'est pas un tableau, type reçu:', typeof data, '; Valeur:', data);
                    if (noResults) noResults.style.display = "block";
                }
            })
            .catch(error => {
                console.error('Erreur:', error);
                if (noResults) noResults.style.display = "block";
            });
        });
    }
});
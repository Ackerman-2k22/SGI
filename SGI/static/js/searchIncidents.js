const searchField = document.querySelector("#searchField");

const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
const paginationContainer = document.querySelector(".pagination-container");
tableOutput.style.display = "none";
const noResults = document.querySelector(".no-results"); // Sélection de l'élément .no-results
const tbody = document.querySelector(".table-body");

searchField.addEventListener("keyup", (e) => {
  const searchValue = e.target.value;

  if (searchValue.trim().length > 0) {
    paginationContainer.style.display = "none";
    tbody.innerHTML = "";
    fetch("/search-incidents", {
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      method: "POST",
      body: JSON.stringify({ searchText: searchValue }),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("data", data);
        appTable.style.display = "none";
        tableOutput.style.display = "block";

        if (data.length === 0) {
          if (noResults) { // Vérifie si l'élément .no-results existe
            noResults.style.display = "block";
          }
          tableOutput.style.display = "none";
        } else {
          if (noResults) { // Vérifie si l'élément .no-results existe
            noResults.style.display = "none";
          }
          data.forEach((item) => {
            tbody.innerHTML += `
                <tr>
                <td>${item.id}</td>
                <td>${item.client__username}</td>
                <td>${item.description}</td>
                <td>${item.category}</td>
                <td>${item.created_at}</td>
                <td>${item.status}</td>
                <td>${item.assigned_agent}</td>
                <td>${item.comment}</td>
                <td>${item.resolved_at}</td>
                <td><a href="/edit-incidents/${item.id}" class="btn btn-secondary btn-sm">Edit</a></td>
                </tr>`;
          });
        }
      });
  } else {
    tableOutput.style.display = "none";
    appTable.style.display = "block";
    paginationContainer.style.display = "block";
  }
});

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
const renderChart = (data, labels, chartId, title) => {
    var ctx = document.getElementById("myChart").getContext("2d");
    var myChart = new Chart(ctx, {
      type: "doughnut",
      data: {
        labels: labels,
        datasets: [
          {
            label: title,
            data: data,
            backgroundColor: [
              "rgba(255, 99, 132, 0.2)",
              "rgba(54, 162, 235, 0.2)",
              "rgba(255, 206, 86, 0.2)",
              "rgba(75, 192, 192, 0.2)",
              "rgba(153, 102, 255, 0.2)",
              "rgba(255, 159, 64, 0.2)",
            ],
            borderColor: [
              "rgba(255, 99, 132, 1)",
              "rgba(54, 162, 235, 1)",
              "rgba(255, 206, 86, 1)",
              "rgba(75, 192, 192, 1)",
              "rgba(153, 102, 255, 1)",
              "rgba(255, 159, 64, 1)",
            ],
            borderWidth: 1,
          },
        ],
      },
      options: {
        title: {
          display: true,
          text: title,
        },
      },
    });
};



const getChartData = () => {
  console.log("fetching");
  fetch("/incident_category_summary")
    .then((res) => res.json())
    .then((results) => {
      console.log("results", results);
      // Données par catégorie
      const categoryData = results.incident_category_data;
      const categoryLabels = Object.keys(categoryData);
      const categoryValues = Object.values(categoryData);
      renderChart(categoryValues, categoryLabels, "myChart", "Incidents per category");

      // Données par statut
      const statusData = results.incident_status_data;
      const statusLabels = Object.keys(statusData);
      const statusValues = Object.values(statusData);
      renderChart(statusValues, statusLabels, "myStatusChart", "Incidents per statut");

      // Données par agent assigné
      const agentData = results.incident_agent_data;
      const agentLabels = Object.keys(agentData);
      const agentValues = Object.values(agentData);
      renderChart(agentValues, agentLabels, "myAgentChart", "Incidents per assigned agent");

      // Données par mois
      const monthData = results.incident_month_data;
      const monthLabels = Object.keys(monthData);
      const monthValues = Object.values(monthData);
      renderChart(monthValues, monthLabels, "myMonthChart", "Incidents per months");
    });
/*
    // Données par catégorie
  renderChart(categoryValues, categoryLabels, "myChart", "Incidents per category");

  // Données par statut
  renderChart(statusValues, statusLabels, "myStatusChart", "Incidents per statut");

  // Données par agent assigné
  renderChart(agentValues, agentLabels, "myAgentChart", "Incidents per assigned agent");

  // Données par mois
  renderChart(monthValues, monthLabels, "myMonthChart", "Incidents per months");
  */
};

document.addEventListener('DOMContentLoaded', getChartData);
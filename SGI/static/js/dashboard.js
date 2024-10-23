document.addEventListener('DOMContentLoaded', () => {
    const filterWeekBtn = document.getElementById('filter-week');
    const filterMonthBtn = document.getElementById('filter-month');

    if (filterWeekBtn && filterMonthBtn) {
        filterWeekBtn.addEventListener('click', () => updateDashboard('week'));
        filterMonthBtn.addEventListener('click', () => updateDashboard('month'));
    }

    getDashboardData();
});

const renderLineChart = (data, labels, chartId, title) => {
    if (window.myLineChart instanceof Chart && typeof window.myLineChart.destroy === 'function') {
        window.myLineChart.destroy();
    }

    const ctx = document.getElementById(chartId).getContext("2d");
    window.myLineChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: title,
                data: data,
                fill: false,
                borderColor: "rgba(75, 192, 192, 1)",
                tension: 0.1
            }]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: title
                }
            },
            scales: {
                y: { 
                    beginAtZero: true
                }
            }
        }
    });
};
const updateDashboard = (filter) => {
    fetch("/dashboard_data_summary")
    .then(res => res.json())
    .then(results => {
        const dataKey = filter === 'week' ? 'incident_week_data' : 'incident_month_data';
        const { data, labels } = results[dataKey];
        renderLineChart(data, labels, "myLineChart", `Incidents per ${filter}`);
    })
    .catch(error => {
        console.error("Error fetching dashboard data:", error);
    });
};

const getDashboardData = () => {
    updateDashboard('month'); 
};
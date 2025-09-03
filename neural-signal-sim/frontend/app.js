const BAR_EL = document.getElementById('barChart');
let barChart = new Chart(BAR_EL, {
  type: 'bar',
  data: {
    labels: [],
    datasets: [{
      label: 'Spikes (last 60s)',
      data: [],
    }]
  },
  options: {
    responsive: true,
    animation: false,
    scales: {
      y: { beginAtZero: true }
    }
  }
});

async function refresh() {
  try {
    const res = await fetch('/stats?window_seconds=60');
    const stats = await res.json();
    const labels = stats.per_neuron.map(n => 'Neuron ' + n.neuron_id);
    const counts = stats.per_neuron.map(n => n.count);

    barChart.data.labels = labels;
    barChart.data.datasets[0].data = counts;
    barChart.update();

    document.getElementById('totalSpikes').textContent = stats.total_spikes.toLocaleString();
  } catch (e) {
    console.error(e);
  }
}

setInterval(refresh, 1000);
refresh();

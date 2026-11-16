const dataElement_rotacion = document.getElementById("rotacion-data");
if (!dataElement_rotacion) {
    console.error("No se encontró rotacion-data");
}

const rotacion = JSON.parse(dataElement_rotacion.textContent);
console.log(rotacion)


// Rotación
const rotLabels = rotacion.map(x => x.producto);
const rotData   = rotacion.map(x => x.rotacion);

new Chart(document.getElementById('chart-rotation'),
    {
        type: 'bar',
        data: {
            labels: rotLabels,
            datasets: [{ label: 'Rotación', data: rotData, backgroundColor: '#36a2eb' }]
        },
        options: {
            plugins: {
                legend: { display: false }
            },
            scales: { y: { beginAtZero: true } }
        }
    });

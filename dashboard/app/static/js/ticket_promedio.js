// new Chart(document.getElementById('chart-ticket-global'),
//     {
//         type: 'line', data: {
//             labels: ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
//             datasets: [{
//                 label: 'Ticket Promedio Global', data: [27, 28, 29, 30, 29, 31, 32],
//                 borderColor: '#9966ff', fill: false
//             }]
//         }
//     });


const dataElement_ticket_promedio = document.getElementById("ticket-promedio-data");
if (!dataElement_ticket_promedio) {
    console.error("No se encontró ticket-promedio-data");
}

const ticket_promedio = JSON.parse(dataElement_ticket_promedio.textContent);
console.log(ticket_promedio)


// Rotación
const rootLabels = ticket_promedio.map(x => x.fecha);
const rootData   = ticket_promedio.map(x => x.ticket_promedio);

new Chart(document.getElementById('chart-ticket-global'),
    {
        type: 'line', data: {
            labels: rootLabels,
            datasets: [{
                label: 'Ticket Promedio Global', data: rootData,
                borderColor: '#9966ff', fill: false
            }]
        }
    });

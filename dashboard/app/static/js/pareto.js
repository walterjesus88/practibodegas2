// charts.js - KPIs y análisis avanzado (datos simulados)
// const sample = {
// stores: ['Miraflores','San Isidro','Surco','La Molina','Ate'],
// sales7: [860, 540, 320, 420, 310],
// last7: [3000, 2800, 3200, 2900, 3100, 3300, 3420],
// topProducts: [['Pan Bimbo',420],['Agua 1L',380],['Café',335],['Galletas',280],['Cigarrillos',220]],
// alerts:[{date:'2025-11-03',store:'Miraflores',msg:'Stock bajo: Café (2)',action:'Reponer 20'},{date:'2025-11-02',store:'San Isidro',msg:'Ventas 30% abajo',action:'Revisar turno'}],
// abc:[{p:'Pan Bimbo',c:'A',g:1240},{p:'Agua 1L',c:'A',g:980},{p:'Café',c:'B',g:420},{p:'Galletas',c:'B',g:310},{p:'Chocolates',c:'C',g:90}],
// products:[{p:'Pan Bimbo',sold:420,inventory_avg:20,cost:2.5,price:5.0},{p:'Agua 1L',sold:380,inventory_avg:30,cost:1.0,price:2.5},{p:'Café',sold:335,inventory_avg:15,cost:0.6,price:2.0},{p:'Galletas',sold:280,inventory_avg:25,cost:1.2,price:3.0},{p:'Cigarrillos',sold:220,inventory_avg:40,cost:2.0,price:6.0}],
// ranking:[{store:'Miraflores',sales:3420},{store:'San Isidro',sales:3100},{store:'Surco',sales:2900},{store:'La Molina',sales:2780}] }


Chart.register(window['chartjs-plugin-annotation']);

// ===== Datos simulados =====
const products = [
  {p:'Pan Bimbo', sold:420, inventory_avg:20, cost:2.5, price:5.0},
  {p:'Agua 1L', sold:380, inventory_avg:30, cost:1.0, price:2.5},
  {p:'Café', sold:335, inventory_avg:15, cost:0.6, price:2.0},
  {p:'Galletas', sold:280, inventory_avg:25, cost:1.2, price:3.0},
  {p:'Cigarrillos', sold:220, inventory_avg:40, cost:2.0, price:6.0},
  {p:'Chocolates', sold:150, inventory_avg:12, cost:1.0, price:2.8},
  {p:'Yogurt', sold:90, inventory_avg:8, cost:0.9, price:2.2},
  {p:'Leche', sold:210, inventory_avg:22, cost:2.0, price:4.0},
  {p:'Snack', sold:160, inventory_avg:18, cost:0.8, price:2.5},
  {p:'Jugo', sold:130, inventory_avg:14, cost:1.0, price:2.2}
];


// Pareto
//ordenar por ventas descendente
const paretoProducts = products.slice().sort((a,b)=>b.sold-a.sold);
// calcular porcentaje acumulado
const paretoVals = paretoProducts.map(x=>x.sold);
const paretoLabels = paretoProducts.map(x=>x.p);

// Calcular porcentaje acumulado
const totalSales = paretoVals.reduce((a,b)=>a+b,0);
let cumulative = 0;
const cumulativePercent = paretoVals.map(v=>{
  cumulative += v;
  return (cumulative / totalSales * 100).toFixed(2);
});


// ===== Encontrar el punto donde se supera el 80% =====
let idx80 = cumulativePercent.findIndex(p => p >= 80);
if (idx80 === -1) idx80 = cumulativePercent.length - 1; // seguridad
const product80 = paretoLabels[idx80];
const topProductsCount = idx80 + 1; // cuántos productos suman el 80%
const topProducts = paretoLabels.slice(0, topProductsCount);

// === Mostrar el resultado con tooltip ===
const infoDiv = document.getElementById('pareto-info');
if (infoDiv) {
  infoDiv.innerHTML = `
    🟢 <strong>${topProductsCount}</strong> productos generan el 80% de las ventas.
    <span title="${topProducts.join(', ')}" style="text-decoration: underline; cursor: help;">
      (ver lista)
    </span>
  `;
} else {
  console.warn('⚠️ No se encontró el elemento con id="pareto-info"');
}

// // Mostrar el mensaje arriba del gráfico
// document.getElementById('pareto-info').innerHTML = 
//   `🟢 <strong>${topProductsCount}</strong> productos generan el <strong>80%</strong> de las ventas.`;

// ===== Crear gráfico Pareto =====
new Chart(document.getElementById('chart-pareto'), {
  type: 'bar',
  data: {
    labels: paretoLabels,
    datasets: [
      {
        label: 'Ventas',
        data: paretoVals,
        backgroundColor: '#4bc0c0'
      },
      {
        label: '% Acumulado',
        data: cumulativePercent,
        type: 'line',
        yAxisID: 'y1',
        borderColor: '#ff6384',
        borderWidth: 2,
        fill: false
      }
    ]
  },
  options: {
    plugins: {
      legend: { position: 'top' },
      annotation: {
        annotations: {
          line80h: { // línea horizontal del 80%
            type: 'line',
            yMin: 80,
            yMax: 80,
            yScaleID: 'y1',
            borderColor: 'red',
            borderWidth: 2,
            borderDash: [6, 6],
            label: {
              content: '80%',
              enabled: true,
              position: 'end'
            }
          },
          line80v: { // línea vertical en el producto del 80%
            type: 'line',
            xMin: idx80,
            xMax: idx80,
            borderColor: 'orange',
            borderWidth: 2,
            borderDash: [6, 6],
            label: {
              content: product80,
              enabled: true,
              rotation: 90,
              position: 'start'
            }
          }
        }
      }
    },
    scales: {
      y: { beginAtZero: true, title: { display: true, text: 'Ventas' } },
      y1: {
        beginAtZero: true,
        position: 'right',
        title: { display: true, text: '% acumulado' },
        min: 0,
        max: 100,
        ticks: { callback: value => value + '%' }
      }
    }
  }
});

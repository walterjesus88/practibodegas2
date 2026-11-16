// charts.js - KPIs y análisis avanzado (datos simulados)
const sample = {
stores: ['Miraflores','San Isidro','Surco','La Molina','Ate'],
sales7: [860, 540, 320, 420, 310],
last7: [3000, 2800, 3200, 2900, 3100, 3300, 3420],
topProducts: [['Pan Bimbo',420],['Agua 1L',380],['Café',335],['Galletas',280],['Cigarrillos',220]],
alerts:[{date:'2025-11-03',store:'Miraflores',msg:'Stock bajo: Café (2)',action:'Reponer 20'},{date:'2025-11-02',store:'San Isidro',msg:'Ventas 30% abajo',action:'Revisar turno'}],
abc:[{p:'Pan Bimbo',c:'A',g:1240},{p:'Agua 1L',c:'A',g:980},{p:'Café',c:'B',g:420},{p:'Galletas',c:'B',g:310},{p:'Chocolates',c:'C',g:90}],
products:[{p:'Pan Bimbo',sold:420,inventory_avg:20,cost:2.5,price:5.0},{p:'Agua 1L',sold:380,inventory_avg:30,cost:1.0,price:2.5},{p:'Café',sold:335,inventory_avg:15,cost:0.6,price:2.0},{p:'Galletas',sold:280,inventory_avg:25,cost:1.2,price:3.0},{p:'Cigarrillos',sold:220,inventory_avg:40,cost:2.0,price:6.0}],
ranking:[{store:'Miraflores',sales:3420},{store:'San Isidro',sales:3100},{store:'Surco',sales:2900},{store:'La Molina',sales:2780}] }


Chart.register(window['chartjs-plugin-annotation']);

// ===== Datos simulados =====
const productso = [
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




// // Rotación
// const rotLabels = products.map(x=>x.p);
// const rotData = products.map(x=>(x.sold/x.inventory_avg).toFixed(2));
// new Chart(document.getElementById('chart-rotation'), {type:'bar', data:{labels:rotLabels,datasets:[{label:'Rotación',data:rotData,backgroundColor:'#36a2eb'}]}, options:{plugins:{legend:{display:false}},scales:{y:{beginAtZero:true}}}});

// Margen
const marginLabels = productso.slice(0,5).map(x=>x.p);
const marginData = productso.slice(0,5).map(x=>(((x.price-x.cost)/x.price)*100).toFixed(1));
new Chart(document.getElementById('chart-margin'), {type:'bar', data:{labels:marginLabels,datasets:[{label:'Margen %',data:marginData,backgroundColor:'#ffce56'}]}, options:{indexAxis:'y',plugins:{legend:{display:false}},scales:{x:{beginAtZero:true}}}});




// new Chart(document.getElementById('chart-pareto2'),
//  {type:'line', 
//   data:{labels:paretoLabels,
//         datasets:[{label:'Ventas',data:paretoVals,borderColor:'#4bc0c0',fill:false}]},
//         options:{plugins:{legend:{display:false}},scales:{y:{beginAtZero:true}}}});

// Ranking tiendas
// const ranking = [
//   {store:'Miraflores', sales:3420}, {store:'San Isidro', sales:3100}, {store:'Surco', sales:2900}, {store:'La Molina', sales:2780}, {store:'Ate', sales:2600}
// ];
// const rb=document.getElementById('ranking-body'); ranking.forEach((r,i)=>rb.innerHTML+=`<tr><td>${r.store}</td><td>S/${r.sales}</td><td>#${i+1}</td></tr>`);



//top productos (doughnut)
const prodCtx = document.getElementById('chart-top-products').getContext('2d');
new Chart(prodCtx, {type:'doughnut',data:{labels:sample.topProducts.map(x=>x[0]),datasets:[{data:sample.topProducts.map(x=>x[1])}]},options:{plugins:{legend:{position:'bottom'}}}});

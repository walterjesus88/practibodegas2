// main.js - navegación del sidebar y utilidades básicas
document.addEventListener('DOMContentLoaded', ()=>{
const buttons = document.querySelectorAll('.nav-btn');
const pages = document.querySelectorAll('.page');
buttons.forEach(b=>{
b.addEventListener('click', ()=>{
buttons.forEach(x=>x.classList.remove('active'));
b.classList.add('active');
const t = b.dataset.target;
pages.forEach(p=>{ p.classList.toggle('active', p.id===t) });
})
});


//document.getElementById('refresh-btn').addEventListener('click', ()=> location.reload());
document.getElementById('simulate-ai').addEventListener('click', ()=> {
// disparar recarga de datos simulados en ai_analysis
if(window.aiSimulate) window.aiSimulate();
})
});
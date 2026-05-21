// More compatible frontend: fetch JSON datasets and initialize on DOMContentLoaded
const $ = sel => document.querySelector(sel);

function normalize(s){ return s.toLowerCase().replace(/[^a-z0-9\s]/g,' ').trim(); }

function makeApp(acbData, beersData){
  const drugsEl = $('#drugs');
  const conditionsEl = $('#conditions');
  const runBtn = $('#run');
  const clearBtn = $('#clear');
  const acbDetail = $('#acbDetail');
  const beersDetail = $('#beersDetail');
  const summaryHtml = $('#summaryHtml');

  function computeACB(drugs){
    let total=0; const details=[];
    for(const d of drugs){
      const n=normalize(d);
      const entry = acbData[n] || null;
      const score = entry ? entry.score : 0;
      details.push({input:d,normalized:n,score}); total+=score;
    }
    return {total,details};
  }

  function checkBeers(drugs){
    const hits = [];
    for(const d of drugs){
      const n=normalize(d);
      if(beersData[n]) hits.push({input:d,issues:beersData[n]});
    }
    return hits;
  }

  function renderResults(drugs, conditions){
    const acb = computeACB(drugs);
    const beers = checkBeers(drugs);

    summaryHtml.innerHTML = `Total medicines: <strong>${drugs.length}</strong><br/>`+
      `Total ACB: <strong>${acb.total}</strong> ${acb.total>=3?'<span class="flag" style="color:var(--bad)">HIGH RISK</span>':''}`+
      `${beers.length?'<br/><em style="color:var(--warn)">'+beers.length+' Beers flags</em>':''}`;

    acbDetail.innerHTML = '';
    const pre = document.createElement('pre');
    pre.textContent = acb.details.map(d=>`${d.input} -> ${d.normalized}: ACB ${d.score}`).join('\n');
    acbDetail.appendChild(pre);

    beersDetail.innerHTML='';
    if(beers.length===0){ beersDetail.textContent='No immediate Beers flags found for entered names.' }
    else{
      const ul = document.createElement('div');
      for(const b of beers){
        const div = document.createElement('div');
        div.innerHTML = `<strong>${b.input}</strong>: ${b.issues.join('; ')}`;
        ul.appendChild(div);
      }
      beersDetail.appendChild(ul);
    }
  }

  runBtn.addEventListener('click', ()=>{
    const raw = drugsEl.value||''; const condRaw = conditionsEl.value||'';
    const drugs = raw.split(',').map(s=>s.trim()).filter(Boolean);
    if(drugs.length===0){ alert('Enter at least one medicine'); return; }
    renderResults(drugs, condRaw.split(',').map(s=>s.trim()).filter(Boolean));
  });

  clearBtn.addEventListener('click', ()=>{ drugsEl.value=''; conditionsEl.value=''; summaryHtml.textContent='No results yet. Click Run check.'; acbDetail.textContent='—'; beersDetail.textContent='—'; });

  // Auto-fill demo
  drugsEl.value = 'amitriptyline, diazepam, omeprazole, lisinopril';
  conditionsEl.value = '';
  renderResults(drugsEl.value.split(',').map(s=>s.trim()), []);
}

// Fetch datasets and initialize
Promise.all([
  fetch('./data/acb.json').then(r=>r.ok? r.json() : {}),
  fetch('./data/beers.json').then(r=>r.ok? r.json() : {})
]).then(([acbData, beersData])=>{
  document.addEventListener('DOMContentLoaded', ()=> makeApp(acbData, beersData));
}).catch(err=>{
  console.error('Failed to load datasets', err);
  // still try to initialize with empty datasets
  document.addEventListener('DOMContentLoaded', ()=> makeApp({}, {}));
});

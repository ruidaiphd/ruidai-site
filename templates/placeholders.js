const NS = 'http://www.w3.org/2000/svg';
const el = (t, a) => { const e = document.createElementNS(NS, t); for (const k in a) e.setAttribute(k, a[k]); return e; };
const rnd = (s => () => (s = s * 16807 % 2147483647) / 2147483647)(42);

const ART = [
  g => [['#d99a2b',110,95],['#5fa8d3',275,110],['#7fb069',190,215]].forEach(([col,cx,cy]) => {
    for (let i = 0; i < 22; i++) { const a = rnd()*6.28, r = rnd()*52;
      g.appendChild(el('circle',{cx:cx+Math.cos(a)*r, cy:cy+Math.sin(a)*r, r:2.4, fill:col, 'fill-opacity':.55})); } }),
  g => { for (let i=0;i<4;i++) g.appendChild(el('line',{x1:45,y1:40+i*55,x2:370,y2:40+i*55,stroke:'#2a2a33'}));
    for (let i=0;i<70;i++){ const px=55+rnd()*300, py=250-(px-55)*.45-rnd()*90;
      g.appendChild(el('circle',{cx:px,cy:py,r:3,fill:'#d99a2b','fill-opacity':.5})); }
    g.appendChild(el('path',{d:'M55 240 L360 95',stroke:'#e8e4d7','stroke-width':1.6,fill:'none'})); },
  g => { for (let i=0;i<8;i++){
      g.appendChild(el('rect',{x:38,y:34+i*29,width:108,height:20,rx:2,fill:'#22222b'}));
      g.appendChild(el('rect',{x:254,y:34+i*29,width:108,height:20,rx:2,fill:'#22222b'}));
      const t=34+((i*3)%8)*29;
      g.appendChild(el('path',{d:`M146 ${44+i*29} C 200 ${44+i*29}, 200 ${t+10}, 254 ${t+10}`,stroke:'#d99a2b','stroke-opacity':.5,fill:'none'})); } },
  g => { g.appendChild(el('rect',{x:40,y:28,width:140,height:244,rx:3,fill:'#1e1e26'}));
    for (let i=0;i<17;i++) g.appendChild(el('rect',{x:52,y:42+i*13,width:40+rnd()*76,height:4,rx:2,fill:'#3a3a46'}));
    ['#d99a2b','#5fa8d3','#7fb069','#c96f6f'].forEach((col,i)=>{
      g.appendChild(el('rect',{x:226,y:40+i*60,width:134,height:44,rx:3,fill:col,'fill-opacity':.16,stroke:col,'stroke-opacity':.5}));
      g.appendChild(el('rect',{x:238,y:54+i*60,width:62,height:4,rx:2,fill:col,'fill-opacity':.7}));
      g.appendChild(el('path',{d:`M180 ${100+i*20} C 205 ${100+i*20}, 205 ${62+i*60}, 226 ${62+i*60}`,stroke:col,'stroke-opacity':.4,fill:'none'})); }); },
  g => { for (let i=0;i<7;i++) g.appendChild(el('line',{x1:30,y1:40+i*36,x2:370,y2:40+i*36,stroke:'#26262f'}));
    ['#d99a2b','#5fa8d3','#7fb069'].forEach((col,r)=>{
      for (let i=0;i<9;i++) g.appendChild(el('rect',{x:34+i*38,y:30+r*80,width:30,height:18,rx:2,fill:col,'fill-opacity':.12+rnd()*.5})); }); }
];

document.querySelectorAll('[id^="ph"]').forEach(g => {
  const i = +g.id.slice(2);
  if (!Number.isNaN(i)) ART[i % ART.length](g);
});

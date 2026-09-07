const fs=require('fs'), path=require('path');
function stub(name){
  const f=function(){ return stub('call'); };
  return new Proxy(f,{
    get(t,p){
      if(p==='then'||p==='Symbol(Symbol.toPrimitive)') return undefined;
      if(p===Symbol.toPrimitive) return ()=>0;
      if(p==='length') return 0;
      if(p==='style'||p==='classList'||p==='dataset') return stub(p);
      if(p==='textContent'||p==='innerHTML'||p==='value'||p==='className') return '';
      if(p==='children'||p==='childNodes') return [];
      return stub(String(p));
    },
    set(){ return true; },
    apply(){ return stub('ret'); },
    construct(){ return stub('new'); },
    has(){ return true; }
  });
}
const file=process.argv[2];
const html=fs.readFileSync(file,'utf8').replace(/<!--[\s\S]*?-->/g,'');
const scripts=[...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)].map(m=>m[1]).filter(s=>s.trim());
const g={ window:{}, document:stub('document'), localStorage:stub('ls'),
  matchMedia:()=>({matches:false,addEventListener(){},addListener(){}}),
  requestAnimationFrame:()=>0, cancelAnimationFrame(){}, setTimeout:()=>0, clearTimeout(){},
  setInterval:()=>0, clearInterval(){}, Image:function(){ return stub('img'); },
  IntersectionObserver:function(){ return stub('io'); }, MutationObserver:function(){ return stub('mo'); },
  navigator:{maxTouchPoints:0,userAgent:'node'}, location:{href:'',pathname:'/'},
  console:{log(){},warn(){},error(){}}, getComputedStyle:()=>stub('cs'),
  addEventListener(){}, removeEventListener(){}, dispatchEvent(){return true;},
  innerWidth:1280, innerHeight:800, devicePixelRatio:1, scrollTo(){}, open(){},
  CustomEvent:function(){return stub('ev');}, Event:function(){return stub('ev');},
  KeyboardEvent:function(){return stub('ev');}, WheelEvent:function(){return stub('ev');},
  PointerEvent:function(){return stub('ev');}, MouseEvent:function(){return stub('ev');},
  Panzoom:undefined, alert(){}, fetch(){return Promise.resolve(stub('res'));} };
g.window=g; g.globalThis=g; g.self=g;
const vm=require('vm'); const ctx=vm.createContext(g);
let failed=null;
for(const src of scripts){
  try{ new vm.Script(src,{filename:path.basename(file)}).runInContext(ctx,{timeout:4000}); }
  catch(e){
    const m=String(e && e.message||e);
    if(/is not defined|is not a function|Cannot read/.test(m)){ failed=m; break; }
  }
}
if(failed){ console.log('FAIL '+path.basename(file)+'  '+failed); process.exit(1); }
console.log('ok   '+path.basename(file));

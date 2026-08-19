import io,sys
OLD='  vp.addEventListener("wheel",function(e){ if(!e.ctrlKey||mode!=="scroll"){return;} e.preventDefault();setStripZoom(stripZoom*(e.deltaY<0?1.12:1/1.12),e.clientY); },{passive:false});'
NEW=('  vp.addEventListener("wheel",function(e){ if(!e.ctrlKey){return;}\n'
     '    e.preventDefault();\n'
     '    if(mode==="scroll"){ setStripZoom(stripZoom*(e.deltaY<0?1.12:1/1.12),e.clientY); }\n'
     '    else { setStageZoom(stageZoom*(e.deltaY<0?1.12:1/1.12)); }\n'
     '  },{passive:false});\n'
     '  zone.addEventListener("wheel",function(e){\n'
     '    if(e.ctrlKey){return;}\n'
     '    e.preventDefault();\n'
     '    var d=(Math.abs(e.deltaY)>=Math.abs(e.deltaX)?e.deltaY:e.deltaX);\n'
     '    if(!d){return;}\n'
     '    zscroll+=d;\n'
     '    var step=Math.trunc(zscroll/40); if(!step){return;}\n'
     '    zscroll-=step*40;\n'
     '    var i=Math.max(0,Math.min(TOTAL-1,currentIndex()+step));\n'
     '    if(i!==currentIndex()){ go(i); }\n'
     '  },{passive:false});')
VOLD='var mode="pages",page=0,onCard=null,nodes=[],thumbs=[],toastT=null,marks=[],fit=true,tapAdvance=false,stageZoom=1,stripZoom=1;'
for f in sys.argv[1:]:
    s=io.open(f,encoding='utf-8').read()
    if 'zscroll' in s: print(f,'already patched'); continue
    if OLD not in s or VOLD not in s: print(f,'!! pattern missing - SKIPPED'); continue
    s=s.replace(OLD,NEW,1).replace(VOLD,VOLD[:-1]+',zscroll=0;',1)
    s=s.replace('["Plus, Minus","Zoom the current page"],["0","Reset zoom"]',
                '["Plus, Minus","Zoom the current page"],["0","Reset zoom"],["Control and scroll wheel","Zoom"],["Wheel over the page bar","Previous / next page"]',1)
    s=s.replace('["Control and scroll wheel","Zoom"],["F","Fullscreen"]',
                '["Control and scroll wheel","Zoom"],["Wheel over the page bar","Previous / next page"],["F","Fullscreen"]',1)
    io.open(f,'w',encoding='utf-8').write(s)
    print(f,'patched')

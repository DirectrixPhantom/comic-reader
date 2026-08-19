import io,sys
LIB=io.open('vendor/panzoom.min.js',encoding='utf-8').read()
BLOCK='<script>/* Panzoom 4.5.1 (MIT) - vendored, see banner */\n'+LIB+'\n</script>\n'

OLD_RENDER='''    if(!fit){ im.style.maxHeight="none";im.style.width="100%"; }
    im.style.transform="scale("+stageZoom+")";
    im.src=PAGES[page].src;
    stage.appendChild(im);stage.scrollTop=0;'''
NEW_RENDER='''    if(!fit){ im.style.maxHeight="none";im.style.width="100%"; }
    im.src=PAGES[page].src;
    stage.appendChild(im);stage.scrollTop=0;
    attachPanzoom(im);'''

OLD_ZOOM='  function setStageZoom(z){ if(onCard){return;} stageZoom=Math.max(1,Math.min(4,z));var im=stage.querySelector("img");if(im){ im.style.transform="scale("+stageZoom+")"; }toast(stageZoom===1?"Zoom reset":"Zoom "+stageZoom.toFixed(1)+"x"); }'
NEW_ZOOM='''  /* ---- zoom + pan (Panzoom, vendored; degrades to plain scale if absent) ---- */
  var pz=null;
  function killPanzoom(){ if(pz){ try{pz.destroy();}catch(_){} pz=null; } }
  function attachPanzoom(im){
    killPanzoom();
    if(!window.Panzoom){ im.style.transform="scale("+stageZoom+")"; return; }
    pz=window.Panzoom(im,{
      maxScale:6, minScale:1, startScale:stageZoom, step:0.25,
      contain:"outside", panOnlyWhenZoomed:true, cursor:"auto", animate:true, duration:120,
      /* only swallow pointer events once actually zoomed, so tap-to-advance and
         swipe keep working at 1x */
      handleStartEvent:function(e){ if(pz&&pz.getScale()>1.01){ e.preventDefault(); e.stopPropagation(); } }
    });
    im.addEventListener("panzoomchange",function(e){ stageZoom=e.detail.scale; syncZoomCursor(); });
  }
  function syncZoomCursor(){ var im=stage.querySelector("img"); if(im){ im.style.cursor = stageZoom>1.01?"grab":"auto"; } }
  function setStageZoom(z){ if(onCard){return;}
    stageZoom=Math.max(1,Math.min(6,z));
    if(pz){ if(stageZoom<=1.001){ pz.reset({animate:true}); stageZoom=1; } else { pz.zoom(stageZoom,{animate:true}); } }
    else { var im=stage.querySelector("img"); if(im){ im.style.transform="scale("+stageZoom+")"; } }
    syncZoomCursor();
    toast(stageZoom===1?"Zoom reset":"Zoom "+stageZoom.toFixed(1)+"x"); }'''

def patch(f):
    s=io.open(f,encoding='utf-8').read()
    if 'Panzoom 4.5.1' in s: return f+' already has panzoom'
    for pat in (OLD_RENDER,OLD_ZOOM):
        if pat not in s: return f+' !! pattern missing - SKIPPED'
    s=s.replace(OLD_RENDER,NEW_RENDER,1).replace(OLD_ZOOM,NEW_ZOOM,1)
    # destroy the instance when leaving pages mode
    s=s.replace('  function setMode(m){','  function setMode(m){ if(m!=="pages"){ killPanzoom(); }',1)
    # inline the library ahead of the main script
    i=s.index('<script>',s.index('window.CONFIG'))
    s=s[:i]+BLOCK+s[i:]
    io.open(f,'w',encoding='utf-8').write(s)
    return f+' patched (%.1f KB)'%(len(s.encode())/1024)
for f in sys.argv[1:]: print(patch(f))

AVAIABLE_EVENTS = {"ondevicemotion","ondeviceorientation","ondeviceorientationabsolute","onabort","onblur","onfocus","oncancel","onauxclick","onbeforeinput","onbeforematch","onbeforetoggle","oncanplay","oncanplaythrough","onchange","onclick","onclose","oncontentvisibilityautostatechange","oncontextlost","oncontextmenu","oncommand","oncontextrestored","oncopy","oncuechange","oncut","ondblclick","ondrag","ondragend","ondragenter","ondragexit","ondragleave","ondragover","ondragstart","ondrop","ondurationchange","onemptied","onended","onformdata","oninput","oninvalid","onkeydown","onkeypress","onkeyup","onload","onloadeddata","onloadedmetadata","onloadstart","onmousedown","onmouseenter","onmouseleave","onmousemove","onmouseout","onmouseover","onmouseup","onwheel","onpaste","onpause","onplay","onplaying","onprogress","onratechange","onreset","onresize","onscroll","onscrollend","onsecuritypolicyviolation","onseeked","onseeking","onselect","onslotchange","onstalled","onsubmit","onsuspend","ontimeupdate","onvolumechange","onwaiting","onselectstart","onselectionchange","ontoggle","onpointercancel","onpointerdown","onpointerup","onpointermove","onpointerout","onpointerover","onpointerenter","onpointerleave","onpointerrawupdate","ongotpointercapture","onlostpointercapture","onmozfullscreenchange","onmozfullscreenerror","onanimationcancel","onanimationend","onanimationiteration","onanimationstart","ontransitioncancel","ontransitionend","ontransitionrun","ontransitionstart","onwebkitanimationend","onwebkitanimationiteration","onwebkitanimationstart","onwebkittransitionend","onerror","onafterprint","onbeforeprint","onbeforeunload","onhashchange","onlanguagechange","onmessage","onmessageerror","onoffline","ononline","onpagehide","onpageshow","onpopstate","onrejectionhandled","onstorage","onunhandledrejection","onunload","ongamepadconnected","ongamepaddisconnected"}

GET_CSS_SELECTOR_PAYLOAD = """
window.__getCssSelectorShort = (el) => {
  let path = [], parent;
  while (parent = el.parentNode) {
    let tag = el.tagName, siblings;

    // Ignore #text node name
    if(!tag) {
      el = parent;
      continue;
    }

    path.unshift(
      el.id ? `#${el.id}` : (
        siblings = parent.children,
        [].filter.call(siblings, sibling => sibling.tagName === tag).length === 1 ? tag :
        `${tag}:nth-child(${1+[].indexOf.call(siblings, el)})`
      )
    );

    el = parent;
  };
  return `${path.join(' > ')}`
};"""

EVENT_RECORD_PAYLOAD = """
if(!window.__userEvents){
window.__userEvents = [];

""" \
+ GET_CSS_SELECTOR_PAYLOAD + \
"""
const blacklisted_props = [/MOZ_.*/, /DOM_.*/]

function htmlSelectorSanitize(ob){
    let x = {};
    if(Array.isArray(ob))
      x = [];
    
    for (let k in ob){
      if(blacklisted_props.some(rx => rx.test(k))){
        console.log('Skipping blacklisted prop', k);
        continue;
      }

      // console.log('Sanitizing key', k, ob[k]);
      if(ob[k] === null || ob[k] === undefined)
        x[k] = ob[k];
      else if(typeof ob[k] === 'object' && (ob[k].tagName || ob[k].nodeName))
        x[k] = window.__getCssSelectorShort(ob[k]);
      else if(Array.isArray(ob[k]) || (typeof ob[k] === 'object' && ob[k] !== null && !(ob[k] instanceof Window || ob[k].self))){
        x[k] = htmlSelectorSanitize(ob[k])
      }
      else if(typeof ob[k] !== 'function')
        x[k] = ob[k];
    }
    return x;
}

function record(type, e, parentIframes = []) {
    let ob = {}
    Object.keys(e.__proto__).forEach(k => {
        ob[k] = e[k]
    })       
    
    console.log('Sanitizing event', e, ob);
    let y = htmlSelectorSanitize(ob);
    window.__userEvents.push({
        type, 
        event: y, 
        target: window.__getCssSelectorShort(e.target),
        parentIframes,
        time: Date.now(),
    });
}

function injectIframeListeners(key, parentIframes = []){
  //If parentIframe is not provided, start from document
  let iframes = null
  if(!parentIframes || parentIframes.length === 0)
    iframes = document.getElementsByTagName('iframe');
  else
    iframes = parentIframes.at(-1).getElementsByTagName('iframe');

    for (let i = 0; i < iframes.length; i++) {
        try {
            iframes[i].contentWindow.addEventListener(key.slice(2), e => {
                newIframes = [
                    ...parentIframes, 
                    window.__getCssSelectorShort(iframes[i])
                ];
                record(key, e, newIframes);
                injectIframeListeners(key, newIframes);
            })
        } catch (err) {
            console.error('Could not attach event listener to iframe:', key, iframes[i], err);
        }
    }
}

///EVENTS///.forEach(key => {
    window.addEventListener(key.slice(2), e => {
        record(key, e);
    })
    injectIframeListeners(key);
});
}"""

EVENT_LIST_PAYLOAD = """
var events = window.__userEvents || [];
window.__userEvents = [];
return events;
"""

DRAG_DROP_PAYLOAD = """
window.__html5DragAndDrop = function(src, tgt) {
    const dataTransfer = new DataTransfer();

    console.log("Starting drag and drop from", src, "to", tgt);
    let results = [0,0,0,0];

    results[0] = src.dispatchEvent(new DragEvent("dragstart", {
        dataTransfer,
        bubbles: true,
        cancelable: true
    }));

    results[1] = tgt.dispatchEvent(new DragEvent("dragover", {
        dataTransfer,
        bubbles: true,
        cancelable: true
    }));

    results[2] = tgt.dispatchEvent(new DragEvent("drop", {
        dataTransfer,
        bubbles: true,
        cancelable: true
    }));

    results[3] = src.dispatchEvent(new DragEvent("dragend", {
        dataTransfer,
        bubbles: true,
        cancelable: true
    }));

    console.log("Drag and drop results:", results);
}
"""

EVENT_LISTENER_INJECTED_PAYLOAD = """return !!window.__userEvents;"""

def get_event_recorder_payload(recordable_events: list[str] | None):
    if recordable_events is None:
        events = AVAIABLE_EVENTS
    else:
        events = [x for x in recordable_events if x in AVAIABLE_EVENTS]
        
    return EVENT_RECORD_PAYLOAD.replace('///EVENTS///', str(events))
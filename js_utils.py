AVAIABLE_EVENTS = {"ondevicemotion","ondeviceorientation","ondeviceorientationabsolute","onabort","onblur","onfocus","oncancel","onauxclick","onbeforeinput","onbeforematch","onbeforetoggle","oncanplay","oncanplaythrough","onchange","onclick","onclose","oncontentvisibilityautostatechange","oncontextlost","oncontextmenu","oncommand","oncontextrestored","oncopy","oncuechange","oncut","ondblclick","ondrag","ondragend","ondragenter","ondragexit","ondragleave","ondragover","ondragstart","ondrop","ondurationchange","onemptied","onended","onformdata","oninput","oninvalid","onkeydown","onkeypress","onkeyup","onload","onloadeddata","onloadedmetadata","onloadstart","onmousedown","onmouseenter","onmouseleave","onmousemove","onmouseout","onmouseover","onmouseup","onwheel","onpaste","onpause","onplay","onplaying","onprogress","onratechange","onreset","onresize","onscroll","onscrollend","onsecuritypolicyviolation","onseeked","onseeking","onselect","onslotchange","onstalled","onsubmit","onsuspend","ontimeupdate","onvolumechange","onwaiting","onselectstart","onselectionchange","ontoggle","onpointercancel","onpointerdown","onpointerup","onpointermove","onpointerout","onpointerover","onpointerenter","onpointerleave","onpointerrawupdate","ongotpointercapture","onlostpointercapture","onmozfullscreenchange","onmozfullscreenerror","onanimationcancel","onanimationend","onanimationiteration","onanimationstart","ontransitioncancel","ontransitionend","ontransitionrun","ontransitionstart","onwebkitanimationend","onwebkitanimationiteration","onwebkitanimationstart","onwebkittransitionend","onerror","onafterprint","onbeforeprint","onbeforeunload","onhashchange","onlanguagechange","onmessage","onmessageerror","onoffline","ononline","onpagehide","onpageshow","onpopstate","onrejectionhandled","onstorage","onunhandledrejection","onunload","ongamepadconnected","ongamepaddisconnected"}

EVENT_RECORD_PAYLOAD = """
if(!window.__userEvents){
window.__userEvents = [];

var getCssSelectorShort = (el) => {
  let path = [], parent;
  while (parent = el.parentNode) {
    let tag = el.tagName, siblings;
    path.unshift(
      el.id ? `#${el.id}` : (
        siblings = parent.children,
        [].filter.call(siblings, sibling => sibling.tagName === tag).length === 1 ? tag :
        `${tag}:nth-child(${1+[].indexOf.call(siblings, el)})`
      )
    );
    if(el.id)
        break;
    el = parent;
  };
  return `${path.join(' > ')}`.toLowerCase();
};

function record(type, e) {
    let x = {}
    Object.keys(e.__proto__).forEach(k => {
        x[k] = e[k]
    })
    window.__userEvents.push({
        type, 
        event: x, 
        target: getCssSelectorShort(e.target),
        time: Date.now(),
    });
}

///EVENTS///.forEach(key => {
    window.addEventListener(key.slice(2), e => {
            record(key, e);
    })
});
}"""

EVENT_LIST_PAYLOAD = """
var events = window.__userEvents || [];
window.__userEvents = [];
return events;
"""

def get_event_recorder_payload(recordable_events: list[str] | None):
    if recordable_events is None:
        events = AVAIABLE_EVENTS
    else:
        events = [x for x in recordable_events if x in AVAIABLE_EVENTS]
        
    return EVENT_RECORD_PAYLOAD.replace('///EVENTS///', str(events))
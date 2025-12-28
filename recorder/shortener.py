from abc import ABC, abstractmethod

class BaseShortener(ABC):
    def __init__(self, captured_events: list[dict]):
        self.captured_events = captured_events

    @abstractmethod
    def shorten(self):
        ...

class MouseActionsShortener(BaseShortener):

    def _find_previous_event_index(self, start_index, type = None, skip = 0):
        last = skip
        for i in range(start_index, -1, -1):
            if not type or self.captured_events[i].get('type') == type:
                last -= 1
            
            if last < 0:
                return i

    def _enumerate_odd_clicks(self):
        removable_events = set()

        for i, e in enumerate(self.captured_events):
            e_type = e.get('type')
            if e_type == 'onclick':
                delta = self.captured_events[i - 1]['time'] - self.captured_events[i - 2]['time']
                if abs(delta) <= 100:
                    removable_events.add(self._find_previous_event_index(i, 'onmouseup'))
                    removable_events.add(self._find_previous_event_index(i, 'onmousedown'))
                else:
                    removable_events.add(i)
            elif e_type == 'ondblclick':
                removable_events |= {
                    self._find_previous_event_index(i, 'onclick'),
                    self._find_previous_event_index(i, 'onmouseup'),
                    self._find_previous_event_index(i, 'onmousedown'),
                    self._find_previous_event_index(i, 'onclick', 1),
                    self._find_previous_event_index(i, 'onmouseup', 1),
                    self._find_previous_event_index(i, 'onmousedown', 1),
                }
        
        return removable_events

    def shorten(self):
        removable_events = self._enumerate_odd_clicks()
        print(removable_events)

        return [c for i, c in enumerate(self.captured_events) if i not in removable_events]

class WheelActionsShortener(BaseShortener):
    def shorten(self):
        start, end = -1, -1
        summarDeltaY = 0
        for i, e in enumerate(self.captured_events):
            if e['type'] == 'onwheel':
                if start == -1:
                    start = i
                summarDeltaY += e['event']['deltaY']
                end = i
        
        self.captured_events[end]['event']['deltaY'] = summarDeltaY
        self.captured_events[end]['duration'] = self.captured_events[end]['time'] - self.captured_events[start]['time']

        return [e for i, e in enumerate(self.captured_events) if not (start <= i < end)]

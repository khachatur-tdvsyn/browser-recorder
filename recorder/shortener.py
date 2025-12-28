from abc import ABC, abstractmethod

class BaseShortener(ABC):
    def __init__(self, captured_events: list[dict]):
        self.captured_events = captured_events

    @abstractmethod
    def shorten(self):
        ...

class MouseActionsShortener(BaseShortener):

    def _enumerate_odd_clicks(self):
        click_events = []
        removable_events = []

        for i, e in enumerate(self.captured_events):
            e_type = e.get('type')
            if (
                len(click_events) == 0 and e_type == 'onmousedown' or \
                len(click_events) == 1 and e_type == 'onmouseup' or \
                len(click_events) == 2 and e_type == 'onclick'
            ):
                print('Detected', e_type, 'at', e.get('time'), i)
                click_events.append({
                    'index': i,
                    'event': e,
                    'timestamp': e.get('time')
                })
            
            if len(click_events) == 3:
                delta = click_events[1]['timestamp'] - click_events[0]['timestamp']

                if abs(delta) <= 100:
                    print('Delta', delta, 'it is click')
                    removable_events.append(click_events[1]['index'])
                    removable_events.append(click_events[0]['index'])
                else:
                    print('Delta', delta, 'it is long move')
                    removable_events.append(click_events[2]['index'])
                
                click_events.clear()
        
        return removable_events

    def shorten(self):
        removable_events = self._enumerate_odd_clicks()
        print(removable_events)

        return [c for i, c in enumerate(self.captured_events) if i not in removable_events]
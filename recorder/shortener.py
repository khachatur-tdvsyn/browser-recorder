from abc import ABC, abstractmethod


class BaseShortener(ABC):
    def __init__(self, captured_events: list[dict]):
        self.captured_events = captured_events

    @abstractmethod
    def shorten(self): ...


class ClickActionsShortener(BaseShortener):

    def _find_previous_event_index(self, start_index, type=None, skip=0):
        last = skip
        for i in range(start_index, -1, -1):
            if not type or self.captured_events[i].get("type") == type:
                last -= 1

            if last < 0:
                return i

    def _enumerate_odd_clicks(self):
        removable_events = set()

        for i, e in enumerate(self.captured_events):
            e_type = e.get("type")
            if e_type == "onclick":
                delta = (
                    self.captured_events[i - 1]["time"]
                    - self.captured_events[i - 2]["time"]
                )
                if abs(delta) <= 100:
                    removable_events.add(
                        self._find_previous_event_index(i, "onmouseup")
                    )
                    removable_events.add(
                        self._find_previous_event_index(i, "onmousedown")
                    )
                else:
                    removable_events.add(i)
            elif e_type == "ondblclick":
                removable_events |= {
                    self._find_previous_event_index(i, "onclick"),
                    self._find_previous_event_index(i, "onmouseup"),
                    self._find_previous_event_index(i, "onmousedown"),
                    self._find_previous_event_index(i, "onclick", 1),
                    self._find_previous_event_index(i, "onmouseup", 1),
                    self._find_previous_event_index(i, "onmousedown", 1),
                }

        return removable_events

    def shorten(self):
        removable_events = self._enumerate_odd_clicks()
        print(removable_events)

        return [
            c for i, c in enumerate(self.captured_events) if i not in removable_events
        ]


class WheelActionsShortener(BaseShortener):
    def _find_ranges(self):
        ranges = []
        start, end = -1, -1
        is_negative = False

        for i, e in enumerate(self.captured_events):
            e_type = e.get("type")

            if e_type == "onwheel":
                neg = e["event"]["deltaY"] < 0
                if start == -1:
                    start = i
                    is_negative = neg

                end = i

                # Detects wheel scrolling direction change (ex. from up to down)
                if is_negative != neg:
                    ranges.append((start, end))
                    is_negative = neg
                    start, end = -1, -1

            elif (start, end) != (-1, -1):
                ranges.append((start, end))
                start, end = -1, -1
                is_negative = False

        if end != -1:
            ranges.append((start, end))

        return ranges

    def shorten(self):
        time = 0
        ranges = self._find_ranges()

        for r in ranges:
            start, end = r
            summarDeltaY = 0

            for i in range(start, end + 1):
                summarDeltaY += self.captured_events[i]["event"]["deltaY"]

            self.captured_events[end]["event"]["deltaY"] = summarDeltaY
            self.captured_events[end]["duration"] = (
                self.captured_events[end]["time"] - self.captured_events[start]["time"]
            )

        print(ranges)
        return [
            e
            for i, e in enumerate(self.captured_events)
            if not any([start <= i < end for start, end in ranges])
        ]

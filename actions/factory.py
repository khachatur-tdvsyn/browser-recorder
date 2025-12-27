from .base import (
    BaseAction, 
    MouseBaseAction, 
    UnknownAction
)
from .mouse import (
    ClickAction,
    MouseDownAction,
    MouseMoveAction,
    MouseUpAction,
    DoubleClickAction,
    WheelAction,
    DragAction,
    DropAction
)
from .keyboard import (
    KeyDownAction,
    KeyUpAction
)

from .clipboard import (
    CutAction,
    CopyAction,
    PasteAction
)

class ActionFactory:
    avaiable_actions = {
        "onclick": ClickAction,
        "onmousedown": MouseDownAction,
        "onmouseup": MouseUpAction,
        "onmousemove": MouseMoveAction,
        "ondblclick": DoubleClickAction,
        "onwheel": WheelAction,
        "ondragstart": DragAction,
        "ondrop": DropAction,

        "onkeydown": KeyDownAction,
        "onkeyup": KeyUpAction,

        "oncut": CutAction,
        "oncopy": CopyAction,
        "onpaste": PasteAction,
    }

    @classmethod
    def create_action(cls, driver, params, boundary_recorder = None) -> list[BaseAction]:
        action_objects = []
        
        for p in params:
            Action = cls.avaiable_actions.get(p.get("type"), UnknownAction)
            
            additional_args = {}
            if boundary_recorder and issubclass(Action, MouseBaseAction):
                additional_args["boundary_recorder"] = boundary_recorder

            action_objects.append(Action(driver, p, **additional_args))

        return action_objects

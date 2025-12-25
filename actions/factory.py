from .base import BaseAction, UnknownAction
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
    }

    keep_params_actions = {
        DragAction
    }

    @classmethod
    def create_action(cls, driver, params) -> list[BaseAction]:
        action_objects = []
        param_arr = []
        for p in params:
            Action = cls.avaiable_actions.get(p.get("type"))
            if Action:
                if Action in cls.keep_params_actions:
                    param_arr.append(p)
                else:
                    action_params = param_arr + [p] if len(param_arr) > 0 else p
                    param_arr = []
                    
                    action_objects.append(Action(driver, action_params))
            else:
                action_objects.append(UnknownAction(driver, p))

        return action_objects

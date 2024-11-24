from typing import Optional, Dict, Any
from copy import deepcopy
import json


class PromptConstruct:
    def __init__(self, raw_prompt_fname: str, defaults: Optional[Dict[str, Any]] = None) -> None:
        with open(f"./prompts/{raw_prompt_fname}", "r", encoding="utf-8") as raw_prompt_file:
            self.raw_prompt = raw_prompt_file.read()

        if defaults is None:
            self.defaults = {}
        else:
            self.defaults = defaults

    def __call__(self, **kw):
        kwargs = deepcopy(self.defaults)
        kwargs.update(**kw)

        return self.raw_prompt.format(**kwargs)


def get_sysprompt_construct(version: int = 3) -> PromptConstruct:
    fname = f"./prompts/params_v{version}.json"

    with open(fname, "r", encoding="utf-8") as f:
        data = json.load(f)

    return PromptConstruct(**data)
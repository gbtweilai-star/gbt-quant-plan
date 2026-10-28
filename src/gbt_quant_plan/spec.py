"""The capability contract, copied verbatim from the GBT V8 registry.

Do not hand-edit: ``tests/test_spec.py`` pins every field against the
registry snapshot so drift fails the build instead of shipping quietly.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple

_RAW = r"""{
 "name": "quant_plan",
 "domain": "llm",
 "desc": "**压缩与直达**（主人令 2026-10-16 深度蒸馏自 Bonsai 2 27B）：把**压缩体积**与**直达线路**变成她的原生能力。①压缩：每档 bits/weight ⇒ 估算体积（27B × b/w ÷ 8 × 容器开销 1.3）⇒ 能否落在 8GB 级；参考一手读数（ternary PTQ1_0 = 1.75 b/w · 语言模型 7.67GB · 保留 98.2% FP16 · 同体积胜 IQ2_XXS 12 分）。②直达：意图 ⇒ 能力位 ⇒ 车道 ⇒ 端点，每步都有固定落点、不经本机中转。③执行层三层映射（路由/搬运/内存）对接已施工图。铁律：本地不承载任何大模型（主人 2026-10-08 与 10-16 令），端点不许写 127.0.0.1。op=status/plan/layer/route/speed/check（全只读·零作用域）。",
 "handler": "quant_plan",
 "safe": false,
 "external": false,
 "requires_params": false,
 "params": [],
 "params_hint": "",
 "multi_op": true,
 "ops": [
  "status",
  "plan",
  "layer",
  "route",
  "speed",
  "check"
 ],
 "ops_hint": ""
}"""


@dataclass(frozen=True)
class CapSpec:
    """Immutable description of one capability bit."""

    name: str
    domain: str
    desc: str
    handler: str
    safe: bool
    external: bool
    requires_params: bool
    params: Tuple[str, ...] = ()
    params_hint: str = ""
    multi_op: bool = False
    ops: Tuple[str, ...] = ()
    ops_hint: str = ""

    @property
    def gated(self) -> bool:
        """True when the registry marks this bit ``safe: false``.

        Gated does not mean "dangerous"; it means the action can change state
        that cannot be restored by running the inverse action.
        """
        return not self.safe

    @property
    def summary(self) -> str:
        """First clause of the description, for one-line listings."""
        for sep in ("\uff08", "\uff1b", "\u3002", ";"):
            if sep in self.desc:
                head = self.desc.split(sep, 1)[0].strip()
                if head:
                    return head
        return self.desc.strip()

    def as_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "domain": self.domain,
            "desc": self.desc,
            "handler": self.handler,
            "safe": self.safe,
            "gated": self.gated,
            "external": self.external,
            "requires_params": self.requires_params,
            "params": list(self.params),
            "params_hint": self.params_hint,
            "multi_op": self.multi_op,
            "ops": list(self.ops),
            "ops_hint": self.ops_hint,
        }


_data = json.loads(_RAW)

SPEC = CapSpec(
    name=_data["name"],
    domain=_data["domain"],
    desc=_data["desc"],
    handler=_data["handler"],
    safe=_data["safe"],
    external=_data["external"],
    requires_params=_data["requires_params"],
    params=tuple(_data["params"]),
    params_hint=_data["params_hint"],
    multi_op=_data["multi_op"],
    ops=tuple(_data["ops"]),
    ops_hint=_data["ops_hint"],
)

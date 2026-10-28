# quant_plan

**One capability bit from GBT V8, packaged standalone.** No. 141 of 341,
`llm` domain (LLM).

<p>
<img alt="python" src="https://img.shields.io/badge/python-3.9%2B-blue">
<img alt="license" src="https://img.shields.io/badge/license-MIT-green">
<img alt="deps" src="https://img.shields.io/badge/runtime%20dependencies-0-brightgreen">
</p>

> **压缩与直达**（主人令 2026-10-16 深度蒸馏自 Bonsai 2 27B）：把**压缩体积**与**直达线路**变成她的原生能力。①压缩：每档 bits/weight ⇒ 估算体积（27B × b/w ÷ 8 × 容器开销 1.3）⇒ 能否落在 8GB 级；参考一手读数（ternary PTQ1_0 = 1.75 b/w · 语言模型 7.67GB · 保留 98.2% FP16 · 同体积胜 IQ2_XXS 12 分）。②直达：意图 ⇒ 能力位 ⇒ 车道 ⇒ 端点，每步都有固定落点、不经本机中转。③执行层三层映射（路由/搬运/内存）对接已施工图。铁律：本地不承载任何大模型（主人 2026-10-08 与 10-16 令），端点不许写 127.0.0.1。op=status/plan/layer/route/speed/check（全只读·零作用域）。

That description is copied verbatim from the registry. `tests/test_spec.py` pins it,
so documentation drift fails the build instead of shipping quietly.

## What this package actually is

It is the **contract** for one capability: its name, its parameters, the values it
accepts, and whether it can change state that cannot be restored. It is not the
implementation — that lives in the runtime this bit was extracted from.

So `run()` goes through a narrow `Backend` protocol, and the default backend is a
stub that **says so**:

```
status="validated"   backend="stub"   data={"executed": false}
```

Never `status="ok"`. A stub that reports success is worse than no stub, because the
caller stops looking for the real thing.

## Install

```bash
git clone https://github.com/gbtweilai-star/gbt-quant-plan.git
cd gbt-quant-plan
python -m pip install -e ".[dev]"
```

## Use

```bash
python -m gbt_quant_plan info                  # capability card
python -m gbt_quant_plan spec --json           # machine-readable contract
python -m gbt_quant_plan check --payload '{}'
python -m gbt_quant_plan run   --payload '{}'
```

Real `info` output from this machine:

```text
quant_plan  (llm)  v1.0.0
----------------------------------------
**压缩与直达**（主人令 2026-10-16 深度蒸馏自 Bonsai 2 27B）：把**压缩体积**与**直达线路**变成她的原生能力。①压缩：每档 bits/weight ⇒ 估算体积（27B × b/w ÷ 8 × 容器开销 1.3）⇒ 能否落在 8GB 级；参考一手读数（ternary PTQ1_0 = 1.75 b/w · 语言模型 7.67GB · 保留 98.2% FP16 · 同体积胜 IQ2_XXS 12 分）。②直达：意图 ⇒ 能力位 ⇒ 车道 ⇒ 端点，每步都有固定落点、不经本机中转。③执行层三层映射（路由/搬运/内存）对接已施工图。铁律：本地不承载任何大模型（主人 2026-10-08 与 10-16 令），端点不许写 127.0.0.1。op=status/plan/layer/route/speed/check（全只读·零作用域）。

gated      : True   <- needs explicit consent
external   : False
multi-op   : True
params     : (none)
values     : status, plan, layer, route, speed, check
```

Wire a real implementation:

```python
from gbt_quant_plan import run

class MyBackend:
    name = "my-backend"
    def invoke(self, cap, payload):
        return {"cap": cap, "handled": sorted(payload)}

result = run({}, backend=MyBackend())
assert result.status == "ok"
```

## Parameters

| name | required | notes |
|---|---|---|
| — | no | the registry declares no required parameters |

Registry hint (`params_hint`): (empty)

**注册表登记的取值 / 子动作（6 个）**：`status`、`plan`、`layer`、`route`、`speed`、`check`

Types are deliberately absent: the registry does not declare them, and an invented
type is worse than no type, because callers believe it.

## Boundaries

- Gated: this bit is marked `safe: false` in the registry — it can change state that no inverse action restores.
- No external service dependency declared.
- Multi-op (`multi_op: true`): several sub-actions share one name — read `op` before calling.
- No implementation ships here. Bring a backend; the protocol is one method.

## What this is not

Not a wrapper around a hosted API. Not a model. Not a promise that calling it does
anything on its own. It is the typed seam plus the validation, which is the part that
stays correct even when the implementation changes.

## Tests

```bash
python -m pytest
```

```text
20 passed, 3 skipped in 0.11s
```

## Provenance

| field | value |
|---|---|
| capability | `quant_plan` |
| domain | `llm` |
| handler | `quant_plan` |
| safe | `False` (gated = `True`) |
| external | `False` |
| atlas page | [llm/quant_plan](https://github.com/gbtweilai-star/gbt-caps/blob/main/caps/llm/quant_plan.md) |
| full index | [https://github.com/gbtweilai-star/gbt-caps](https://github.com/gbtweilai-star/gbt-caps) |

The parent README says 348 capabilities; an AST pass over the registry enumerates
`341 + 0 unimplemented + 0 disabled = 341`. The extra 7 are historical duplicates.
Numbering here follows 341 and matches the `gbt-caps` index one-to-one.

## License

MIT.

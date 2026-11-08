# XPDL exports (Bizagi)

XPDL 2.2 files in this folder are **generated from BPMN**, not written by the LLM directly.

## Regenerate

From the repository root:

```
python tools/bpmn_to_xpdl.py
```

This reads `Output/` and `XML код/` and writes matching `.xpdl` files here.

## Import in Bizagi Modeler

1. Export/Import → Import → XPDL  
2. Select the `.xpdl` file  
3. Open simulation from the imported diagram  

## Layout

| Folder | Source BPMN |
|--------|-------------|
| `XPDL/Output/` | `Output/*.bpmn` |
| `XPDL/XML код/` | `XML код/*.bpmn` |

Complex constructs (embedded subprocesses, parallel gateways, lanes, timers) are mapped to XPDL 2.2. Always verify the diagram in Bizagi after import.

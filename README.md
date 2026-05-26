# Industrial Research & Development Practice

AI-assisted BPMN 2.0 process optimization toolkit: generates importable Camunda/bpmn.io diagrams and demonstrates enterprise workflows with gateways, swimlanes, subprocesses, and escalation patterns.

Master's thesis work on using artificial intelligence to improve how organizations design, document, and optimize business processes. This repository is not a single desktop application you install and click through. It is a working laboratory: reference materials, executable BPMN models, generation scripts, prompt specifications, and real outputs you can open in standard process modeling tools.

The core idea is straightforward. Business processes are usually described in words, slides, or messy diagrams. BPMN 2.0 turns them into precise, machine-readable models. Large language models can help draft those models faster, but only if you constrain them with clear rules, good examples, and validation. This project builds that constraint layer and shows what comes out on the other side.

---

## What you will find here

Roughly eighty-six files organized into a few deliberate layers:

| Layer | Role |
|-------|------|
| Knowledge base | Curated Camunda BPMN patterns (text + SVG + XML) |
| Specification | System prompt that defines how an LLM must write BPMN |
| Automation | Python script that emits Camunda-compatible `.bpmn` files |
| Case studies | Russian-language timesheet processes with full documentation |
| Deliverables | AI-generated university workflows in the Output folder |

Everything that ends in `.bpmn` is XML. GitHub will show it as XML if you rename or view raw, but the industry standard extension is `.bpmn`. Camunda Modeler, bpmn.io, and Zeebe Modeler import these files directly.

---

## Repository map

### Output/

The showcase folder for thesis deliverables. These diagrams were produced with AI assistance under the rules in `System Prompt/SystemPrompt.md`.

- `random_scholarship_renewal.bpmn` — Scholarship Renewal. A compact linear process: renewal period opens, grades are pulled from the LMS, a business rule checks GPA, accounting confirms payment, scholarship is renewed. Good baseline example.
- `graduate_diploma_issuance.bpmn` — Graduate Diploma Issuance. A much richer university workflow with three swimlanes (Student Office, Academic Department, Registry and Archive), parallel validation against ERP and LMS, eligibility and approval gateways with rejection paths, a five-day SLA timer that escalates to the dean, an embedded registry subprocess (PDF generation, digital signature, archival), and parallel post-issuance notification plus audit logging. This is the “complex” counterpart to the scholarship model.

Open either file at https://demo.bpmn.io/ (Import) or in Camunda Desktop Modeler to see the diagram render immediately.

### System Prompt/

- `SystemPrompt.md` — The contract between human intent and model output. It instructs the model to behave as a senior BPMN 2.0 architect and Camunda expert. Requirements include full `bpmn:definitions`, executable processes, diagram interchange (`bpmndi`) with shapes and edges, valid `sourceRef` / `targetRef` links, and layouts that do not collapse on import. It pushes toward enterprise patterns: parallel gateways, approval chains, timers, subprocesses, lanes, data objects, exception paths, and realistic university domains (LMS, ERP, dean office, diplomas, scholarships, audit trails). The output must be pure XML only — no markdown wrappers — so it can be saved and opened as `.bpmn` without manual cleanup.

This file is the “prompt engineering” artifact supervisors often ask for when they want to know how the AI side works without shipping a custom app.

### BPMN/

A local archive of the famous [Camunda BPMN Examples](https://camunda.com/bpmn/examples/) page (imported May 2026). It is the pattern library the thesis work stands on.

#### BPMN/00-overview.md and BPMN/README.md

Navigation and index. Explain that Camunda has taught BPMN since 2007 and that the examples answer recurring modeling questions across industries.

#### BPMN/01-bpmn-examples/

Eight markdown articles, each linking an SVG diagram and a matching `.bpmn` file:

1. Business Rules and BPMN — when to externalize rules vs embed them in the flow  
2. Dependent Instances — signals, messages, timers between process instances  
3. Four Eyes Principle — dual approval before a request is accepted  
4. Monthly Invoicing — correct vs incorrect pool modeling  
5. Additional Information Required — getting more data after a user task  
6. Processing Batch Orders — marketplace import patterns  
7. Reassigning User Tasks — delegation and reassignment services  
8. Two Step Escalation — timer-based escalation (three alternative solutions)

Each article explains the scenario, shows advantages and disadvantages of the modeling choice, and points to `../images/imageN.svg` and `../xml/imageN.bpmn`.

#### BPMN/02-bpmn-modeling-styles/

Four short style guides for human-readable diagrams:

1. Avoid Crossing Flows  
2. Naming Conventions  
3. Symmetric Modeling  
4. Use Equal Task Sizes  

These are about layout quality — the difference between a diagram a business analyst trusts and one they ignore.

#### BPMN/images/

Thirty SVG files (`image1.svg` … `image30.svg`) plus `manifest.json` and `image-mapping.csv`. The manifest maps each image to its original Camunda filename, section title, caption, and sibling BPMN path. Useful when you need to trace “which XML belongs to which picture in the article.”

#### BPMN/xml/

Thirty Camunda-importable BPMN files (`image1.bpmn` … `image30.bpmn`) and the generator script.

- `generate_bpmn.py` — Python 3 script with no external dependencies beyond the standard library. It defines a `build_process()` function that takes a process id, name, and ordered list of steps (`start`, `end`, `userTask`, `serviceTask`, `businessRuleTask`, gateways, etc.) and writes valid BPMN 2.0 XML with automatic left-to-right layout (bounds and waypoints). A `MODELS` dictionary encodes all thirty diagrams from the Camunda page titles and step labels. Run:

  ```
  cd BPMN/xml
  python generate_bpmn.py
  ```

  to regenerate every `imageN.bpmn`. The README in this folder notes that complex multi-pool diagrams (e.g. Four Eyes, Monthly Invoicing) are simplified linear versions derived from SVG labels; full visual fidelity may require manual refinement in a modeler.

- `README.md` — Table of all thirty files with section and one-line description.

### XML код/

Two hand-crafted BPMN models for Russian timekeeping (табельный учёт), aligned with Bizagi-style source diagrams:

- `табельныйучёт1.bpmn` — HR sub-process: parallel review of personnel orders, sick leave, and timesheets, then payroll statement generation.  
- `табельныйучёт2.bpmn` — Main process with lanes for department and HR, manual time recording, call activity into the sub-process, inclusive gateway merge, transfer to finance, plus data object associations for timesheets and sick leave records.

These are “ground truth” examples from a real administrative domain, not generated by the Camunda script.

### Описания/

Russian and English markdown documentation for the timesheet models:

- `табельныйучёт1.md` — Sub-process walkthrough, parallel split/join, element list, Bizagi lane notes.  
- `табельныйучёт2.md` — Main process narrative, lane responsibilities, link to the sub-process doc.

They bridge informal process knowledge and formal BPMN XML — exactly the gap thesis work tries to close with AI.

---

## How the pieces fit together

```
  [Camunda examples + style guides]  -->  training context for humans and prompts
              |
              v
  [SystemPrompt.md]  -->  rules for LLM-generated BPMN
              |
              v
  [LLM session / Cursor / API]  -->  Output/*.bpmn (university processes)
              |
              v
  [Camunda Modeler / bpmn.io]  -->  visual review, optimization, thesis discussion

  [generate_bpmn.py]  -->  reproducible baseline XML for all 30 reference patterns
  [XML код + Описания]  -->  documented real-world case study (timesheets)
```

The thesis angle: AI does not replace process analysts. It accelerates drafting and exploration if you give it standards (BPMN 2.0), examples (this repo), and strict output rules (system prompt). Optimization then happens on the models — removing redundant steps, parallelizing independent checks, adding escalation and audit paths — which is visible when you compare `random_scholarship_renewal.bpmn` with `graduate_diploma_issuance.bpmn`.

---

## Technology (honest summary)

| Component | What this repo uses |
|-----------|---------------------|
| Notation | BPMN 2.0, Camunda extensions (`modeler:executionPlatform`, Camunda Cloud 8.9) |
| Diagram interchange | `bpmndi` with `dc:Bounds` and `di:waypoint` |
| LLM workflow | Prompt-driven generation via `System Prompt/SystemPrompt.md` (model choice is up to your environment — e.g. GPT-class or Claude-class models in Cursor or API) |
| Scripting | Python 3, `xml` generation via string templates in `generate_bpmn.py` |
| Viewing | Camunda Modeler, bpmn.io, Zeebe Modeler — no custom viewer required |
| Reference data | Camunda GmbH BPMN examples (attributed in BPMN/README.md) |

There is no bundled Node app, no Docker compose, no database. That is intentional: supervisors and reviewers can audit prompts and XML without installing your private application.

---

## Quick start

1. Clone the repository.  
2. Open `Output/graduate_diploma_issuance.bpmn` in [bpmn.io](https://demo.bpmn.io/).  
3. Read `System Prompt/SystemPrompt.md` to see how AI outputs are constrained.  
4. Browse `BPMN/01-bpmn-examples/03-four-eyes-principle.md` and open `BPMN/xml/image6.bpmn` for a classic approval pattern.  
5. Optional: run `python BPMN/xml/generate_bpmn.py` to regenerate reference XML.

---

## Limitations (worth stating in thesis work)

- `generate_bpmn.py` produces single-lane, mostly linear layouts. Rich diagrams like multi-pool Four Eyes are documented in markdown and SVG but simplified in XML.  
- AI-generated files should always be validated in a modeler (orphan flows, overlapping labels, gateway defaults). The diploma process went through layout iteration for that reason.  
- University scenarios in Output are illustrative models, not deployed Camunda workflows with delegates and DMN tables unless you add them separately.

---

## Citation and attribution

- Camunda BPMN examples: https://camunda.com/bpmn/examples/ (archived under `BPMN/`).  
- Timesheet processes: derived from Bizagi-style diagrams documented in `Описания/`.  
- Thesis context: using AI to support business process optimization through formal BPMN modeling.

---

## Contact and context

Industrial Research & Development Practice — master's thesis materials on AI-assisted business process modeling and optimization. For questions about prompts, XML artifacts, or reproduction steps, start with this README, then `System Prompt/SystemPrompt.md`, then the `Output/` and `BPMN/xml/` folders.

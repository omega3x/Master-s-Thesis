# Camunda BPMN XML (generated from diagrams)

Each `imageN.bpmn` corresponds to `../images/imageN.svg` from the [Camunda BPMN Examples](https://camunda.com/bpmn/examples/) archive.

| File | Section | Description |
|------|---------|-------------|
| image1.bpmn | Business Rules and BPMN | Solution — separate rule engine |
| image2.bpmn | Business Rules and BPMN | Wrong way — rules in process |
| image3.bpmn | Dependent Instances | Signal event |
| image4.bpmn | Dependent Instances | Message event |
| image5.bpmn | Dependent Instances | Timer and loop |
| image6.bpmn | Four Eyes Principle | Main solution |
| image7.bpmn | Four Eyes Principle | Collapsed pools |
| image8.bpmn | Four Eyes Principle | LDAP approvers |
| image9.bpmn | Monthly Invoicing | Solution (separate pools) |
| image10.bpmn | Monthly Invoicing | Wrong way (merged) |
| image11.bpmn | Additional Information | Request from user |
| image12.bpmn | Additional Information | Technical service |
| image13.bpmn | Batch Orders | Marketplace import |
| image14.bpmn | Reassign User Tasks | Reassignment service |
| image15.bpmn | Reassign User Tasks | Reassignment rules |
| image16.bpmn | Reassign User Tasks | Implicit reassignment |
| image17.bpmn | Two Step Escalation | Event-based gateways |
| image18.bpmn | Two Step Escalation | Receive task + timers |
| image19.bpmn | Two Step Escalation | Generic timer |
| image20.bpmn | Avoid Crossing Flows | Good layout |
| image21.bpmn | Avoid Crossing Flows | Counter-example |
| image22.bpmn | Naming Conventions | Good example |
| image23.bpmn | Naming Conventions | Generic labels |
| image24.bpmn | Naming Conventions | Counter-example |
| image25.bpmn | Symmetric Modeling | Good example 1 |
| image26.bpmn | Symmetric Modeling | Counter-example 1 |
| image27.bpmn | Symmetric Modeling | Good example 2 |
| image28.bpmn | Symmetric Modeling | Counter-example 2 |
| image29.bpmn | Equal Task Sizes | Good example |
| image30.bpmn | Equal Task Sizes | Counter-example |

## Regenerate

```bash
python generate_bpmn.py
```

## Import

Open any `imageN.bpmn` in Camunda Web Modeler or Desktop Modeler. Diagrams are simplified linear/branch models derived from SVG labels; complex multi-pool diagrams (e.g. image6–9) may need manual refinement for full fidelity.

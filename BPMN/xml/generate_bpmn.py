# -*- coding: utf-8 -*-
import os

OUT = os.path.dirname(os.path.abspath(__file__))


def esc(s):
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def build_process(pid, pname, steps):
    nodes = []
    for i, (kind, name) in enumerate(steps):
        if kind == "start":
            nid = f"Start_{pid}"
        elif kind == "end":
            nid = f"End_{pid}"
        else:
            nid = f"{kind}_{pid}_{i}"
        nodes.append((nid, kind, name))

    flow_list = []
    for i in range(len(nodes) - 1):
        flow_list.append((f"Flow_{pid}_{i}", nodes[i][0], nodes[i + 1][0]))

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL" '
        'xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" '
        'xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" '
        'xmlns:di="http://www.omg.org/spec/DD/20100524/DI" '
        'xmlns:modeler="http://camunda.org/schema/modeler/1.0" '
        f'id="Definitions_{pid}" targetNamespace="http://bpmn.io/schema/bpmn" '
        'exporter="Camunda Web Modeler" modeler:executionPlatform="Camunda Cloud" '
        'modeler:executionPlatformVersion="8.9.0">\n'
    )
    xml += f'  <bpmn:process id="Process_{pid}" name="{esc(pname)}" isExecutable="true">\n'

    tag_map = {
        "start": "startEvent",
        "end": "endEvent",
        "userTask": "userTask",
        "serviceTask": "serviceTask",
        "businessRuleTask": "businessRuleTask",
        "receiveTask": "receiveTask",
        "exclusiveGateway": "exclusiveGateway",
        "parallelGateway": "parallelGateway",
        "intermediateCatchEvent": "intermediateCatchEvent",
        "manualTask": "manualTask",
    }

    for i, (nid, kind, name) in enumerate(nodes):
        tag = tag_map[kind]
        inc = [flow_list[i - 1][0]] if i > 0 else []
        out = [flow_list[i][0]] if i < len(flow_list) else []
        inc_xml = "".join(f"    <bpmn:incoming>{f}</bpmn:incoming>\n" for f in inc)
        out_xml = "".join(f"    <bpmn:outgoing>{f}</bpmn:outgoing>\n" for f in out)
        xml += f"    <bpmn:{tag} id=\"{nid}\" name=\"{esc(name)}\">\n{inc_xml}{out_xml}    </bpmn:{tag}>\n"

    for fid, src, tgt in flow_list:
        xml += f'    <bpmn:sequenceFlow id="{fid}" sourceRef="{src}" targetRef="{tgt}" />\n'
    xml += "  </bpmn:process>\n"

    x0, y0, w, h = 160, 180, 140, 80
    xml += f'  <bpmndi:BPMNDiagram id="Diagram_{pid}">\n'
    xml += f'    <bpmndi:BPMNPlane id="Plane_{pid}" bpmnElement="Process_{pid}">\n'
    for i, (nid, kind, name) in enumerate(nodes):
        x = x0 + i * 170
        if kind in ("start", "end"):
            xml += (
                f'      <bpmndi:BPMNShape id="Shape_{nid}" bpmnElement="{nid}">'
                f'<dc:Bounds x="{x}" y="{y0 + 22}" width="36" height="36"/>'
                f"</bpmndi:BPMNShape>\n"
            )
        elif "ateway" in kind:
            xml += (
                f'      <bpmndi:BPMNShape id="Shape_{nid}" bpmnElement="{nid}" isMarkerVisible="true">'
                f'<dc:Bounds x="{x}" y="{y0 + 15}" width="50" height="50"/>'
                f"</bpmndi:BPMNShape>\n"
            )
        else:
            xml += (
                f'      <bpmndi:BPMNShape id="Shape_{nid}" bpmnElement="{nid}">'
                f'<dc:Bounds x="{x}" y="{y0}" width="{w}" height="{h}"/>'
                f"</bpmndi:BPMNShape>\n"
            )
    for i, (fid, src, tgt) in enumerate(flow_list):
        x1 = x0 + i * 170 + (36 if nodes[i][1] in ("start", "end") else w)
        x2 = x0 + (i + 1) * 170
        y = y0 + 40
        xml += (
            f'      <bpmndi:BPMNEdge id="Edge_{fid}" bpmnElement="{fid}">'
            f'<di:waypoint x="{x1}" y="{y}"/><di:waypoint x="{x2}" y="{y}"/>'
            f"</bpmndi:BPMNEdge>\n"
        )
    xml += "    </bpmndi:BPMNPlane>\n  </bpmndi:BPMNDiagram>\n</bpmn:definitions>\n"
    return xml


def write(num, pname, steps):
    path = os.path.join(OUT, f"image{num}.bpmn")
    with open(path, "w", encoding="utf-8") as f:
        f.write(build_process(f"Image{num}", pname, steps))
    print("OK", path)


MODELS = {
    1: ("Create Bill - solution", [
        ("start", "Bill requested"),
        ("serviceTask", "Compute discount"),
        ("businessRuleTask", "Rule Engine"),
        ("userTask", "Create bill"),
        ("end", "Bill created"),
    ]),
    2: ("Create Bill - wrong way", [
        ("start", "Bill requested"),
        ("exclusiveGateway", "Sum of order?"),
        ("userTask", "Compute discount"),
        ("exclusiveGateway", "customer type?"),
        ("userTask", "Create bill"),
        ("end", "Bill created"),
    ]),
    3: ("Dependent Instances - Signal", [
        ("start", "Check requested"),
        ("serviceTask", "check for running instances"),
        ("exclusiveGateway", "running instances of same customer?"),
        ("serviceTask", "perform credit check"),
        ("end", "credit check performed"),
    ]),
    4: ("Dependent Instances - Message", [
        ("start", "Check requested"),
        ("serviceTask", "check for running instances"),
        ("exclusiveGateway", "running instances?"),
        ("serviceTask", "perform credit check"),
        ("serviceTask", "inform waiting instance"),
        ("end", "credit check performed"),
    ]),
    5: ("Dependent Instances - Timer", [
        ("start", "Check requested"),
        ("serviceTask", "check for running instances"),
        ("exclusiveGateway", "running instances?"),
        ("intermediateCatchEvent", "wait some time"),
        ("serviceTask", "perform credit check"),
        ("end", "credit check performed"),
    ]),
    6: ("Four Eyes Principle", [
        ("start", "Approval requested"),
        ("userTask", "decide on approval (1st stage)"),
        ("exclusiveGateway", "approved?"),
        ("userTask", "decide on approval (2nd stage)"),
        ("exclusiveGateway", "approved?"),
        ("end", "request approved"),
    ]),
    7: ("Four Eyes - collapsed pools", [
        ("start", "Approval requested"),
        ("userTask", "decide on approval (1st stage)"),
        ("exclusiveGateway", "approved?"),
        ("userTask", "decide on approval (2nd stage)"),
        ("exclusiveGateway", "approved?"),
        ("end", "request approved"),
    ]),
    8: ("Four Eyes - LDAP", [
        ("start", "Approval requested"),
        ("serviceTask", "determine 1st and 2nd approver"),
        ("userTask", "decide on approval (1st stage)"),
        ("exclusiveGateway", "approved?"),
        ("userTask", "decide on approval (2nd stage)"),
        ("end", "request approved"),
    ]),
    9: ("Monthly Invoicing - solution", [
        ("start", "Legal Advice requested"),
        ("userTask", "provide legal advice"),
        ("userTask", "register time"),
        ("end", "Request handled"),
    ]),
    10: ("Monthly Invoicing - wrong way", [
        ("start", "Legal Advice requested"),
        ("userTask", "provide legal advice"),
        ("userTask", "register time"),
        ("userTask", "determine billable hours"),
        ("userTask", "create and send invoice"),
        ("end", "Invoice settled"),
    ]),
    11: ("Additional Info - from user", [
        ("start", "some task for the user"),
        ("exclusiveGateway", "additional information required?"),
        ("userTask", "request information (from user)"),
        ("end", "continued"),
    ]),
    12: ("Additional Info - technical service", [
        ("start", "some task for the user"),
        ("exclusiveGateway", "additional information required?"),
        ("serviceTask", "send information request (technical)"),
        ("end", "information received"),
    ]),
    13: ("Batch Orders Marketplace", [
        ("start", "Every 10 minutes"),
        ("serviceTask", "Collect all orders from marketplace"),
        ("userTask", "Check order data"),
        ("exclusiveGateway", "data correct?"),
        ("serviceTask", "Import order to ERP system"),
        ("end", "All orders processed"),
    ]),
    14: ("Reassign - service", [
        ("start", "some user task started"),
        ("serviceTask", "determine assignee"),
        ("userTask", "some user task"),
        ("end", "task completed"),
    ]),
    15: ("Reassign - rules", [
        ("start", "some user task started"),
        ("businessRuleTask", "determine assignee"),
        ("userTask", "some user task"),
        ("end", "task completed"),
    ]),
    16: ("Reassign - implicit", [
        ("start", "some user task started"),
        ("userTask", "some user task"),
        ("end", "task completed"),
    ]),
    17: ("Two Step Escalation - event gateways", [
        ("start", "Pizza wanted"),
        ("userTask", "Order Pizza"),
        ("intermediateCatchEvent", "Pizza received"),
        ("userTask", "Eat Pizza"),
        ("end", "Pizza eaten"),
    ]),
    18: ("Two Step Escalation - receive task", [
        ("start", "Pizza wanted"),
        ("userTask", "Order Pizza"),
        ("receiveTask", "Wait for Pizza"),
        ("userTask", "Eat Pizza"),
        ("end", "Pizza eaten"),
    ]),
    19: ("Two Step Escalation - generic timer", [
        ("start", "Pizza wanted"),
        ("userTask", "Order Pizza"),
        ("exclusiveGateway", "already complained?"),
        ("userTask", "Complain to Delivery Service"),
        ("end", "Order cancelled"),
    ]),
    20: ("Avoid Crossing Flows - good", [
        ("start", "process started"),
        ("userTask", "perform task one"),
        ("exclusiveGateway", "required action?"),
        ("userTask", "perform task two"),
        ("exclusiveGateway", "ok?"),
        ("userTask", "perform task three"),
        ("end", "process finished"),
    ]),
    21: ("Avoid Crossing Flows - counter", [
        ("start", "process started"),
        ("userTask", "perform task one"),
        ("exclusiveGateway", "required action?"),
        ("userTask", "perform task three"),
        ("exclusiveGateway", "ok?"),
        ("userTask", "perform task two"),
        ("end", "process finished"),
    ]),
    22: ("Naming Conventions - good", [
        ("start", "Order received"),
        ("userTask", "Check order"),
        ("exclusiveGateway", "Order data correct?"),
        ("userTask", "Check Order Data"),
        ("end", "Order checked"),
    ]),
    23: ("Naming Conventions - generic", [
        ("start", "Trigger of process"),
        ("userTask", "Object + Verb"),
        ("end", "Object + Past Participle"),
    ]),
    24: ("Naming Conventions - counter", [
        ("start", "Start"),
        ("userTask", "Checking"),
        ("userTask", "set status in database"),
        ("end", "End"),
    ]),
    25: ("Symmetric Modeling - good 1", [
        ("start", "hunger noticed"),
        ("userTask", "choose recipe"),
        ("exclusiveGateway", "desired dish?"),
        ("userTask", "prepare salad"),
        ("userTask", "eat meal"),
        ("end", "hunger satisfied"),
    ]),
    26: ("Symmetric Modeling - counter 1", [
        ("start", "hunger noticed"),
        ("userTask", "choose recipe"),
        ("exclusiveGateway", "desired component?"),
        ("userTask", "cook pasta"),
        ("userTask", "eat meal"),
        ("end", "hunger satisfied"),
    ]),
    27: ("Symmetric Modeling - good 2", [
        ("start", "Order received"),
        ("exclusiveGateway", "Order value above 25000?"),
        ("userTask", "produce fresh product"),
        ("userTask", "Process order"),
        ("userTask", "Ship order"),
        ("end", "Order processed"),
    ]),
    28: ("Symmetric Modeling - counter 2", [
        ("start", "Order received"),
        ("userTask", "use old product from stock"),
        ("exclusiveGateway", "Order value above 25000?"),
        ("userTask", "Package goods"),
        ("userTask", "Ship order"),
        ("end", "Order processed"),
    ]),
    29: ("Equal Task Sizes - good", [
        ("start", "Approval requested"),
        ("userTask", "evaluate request document"),
        ("userTask", "submit decision"),
        ("end", "task completed"),
    ]),
    30: ("Equal Task Sizes - counter", [
        ("start", "Approval requested"),
        ("userTask", "evaluate request document and submit decision"),
        ("end", "task completed"),
    ]),
}

if __name__ == "__main__":
    for num, (pname, steps) in MODELS.items():
        write(num, pname, steps)

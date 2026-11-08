# -*- coding: utf-8 -*-
"""Convert Camunda/bpmn.io BPMN 2.0 XML to XPDL 2.2 for Bizagi Modeler import."""

from __future__ import annotations

import argparse
import os
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

BPMN_NS = "{http://www.omg.org/spec/BPMN/20100524/MODEL}"
BPMNDI_NS = "{http://www.omg.org/spec/BPMN/20100524/DI}"
DC_NS = "{http://www.omg.org/spec/DD/20100524/DC}"
DI_NS = "{http://www.omg.org/spec/DD/20100524/DI}"
XPDL_NS = "http://www.wfmc.org/2009/XPDL2.2"

TASK_TAGS = {
    "userTask",
    "serviceTask",
    "businessRuleTask",
    "manualTask",
    "scriptTask",
    "task",
    "sendTask",
    "receiveTask",
}
EVENT_TAGS = {
    "startEvent",
    "endEvent",
    "intermediateCatchEvent",
    "intermediateThrowEvent",
    "boundaryEvent",
}
GATEWAY_TAGS = {
    "exclusiveGateway",
    "parallelGateway",
    "inclusiveGateway",
    "complexGateway",
    "eventBasedGateway",
}
GATEWAY_TYPES = {
    "exclusiveGateway": "XOR",
    "parallelGateway": "AND",
    "inclusiveGateway": "OR",
    "complexGateway": "COMPLEX",
    "eventBasedGateway": "XOR",
}

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCES = [ROOT / "Output", ROOT / "XML код"]
DEFAULT_OUT = ROOT / "XPDL"


def esc(text: str | None) -> str:
    if text is None:
        return ""
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def attr(elem: ET.Element, name: str, default: str = "") -> str:
    return elem.get(name, default)


def child_text(elem: ET.Element, path: str) -> str | None:
    for child in elem.iter():
        if local(child.tag) == path:
            if child.text:
                return child.text.strip()
    return None


def parse_bounds(diagram: ET.Element | None) -> dict[str, tuple[int, int, int, int]]:
    bounds: dict[str, tuple[int, int, int, int]] = {}
    if diagram is None:
        return bounds
    for shape in diagram.iter(f"{BPMNDI_NS}BPMNShape"):
        ref = attr(shape, "bpmnElement")
        for bounds_elem in shape.iter(f"{DC_NS}Bounds"):
            bounds[ref] = (
                int(float(attr(bounds_elem, "x", "0"))),
                int(float(attr(bounds_elem, "y", "0"))),
                int(float(attr(bounds_elem, "width", "36"))),
                int(float(attr(bounds_elem, "height", "36"))),
            )
    return bounds


def parse_waypoints(diagram: ET.Element | None) -> dict[str, list[tuple[int, int]]]:
    edges: dict[str, list[tuple[int, int]]] = {}
    if diagram is None:
        return edges
    for edge in diagram.iter(f"{BPMNDI_NS}BPMNEdge"):
        ref = attr(edge, "bpmnElement")
        points: list[tuple[int, int]] = []
        for wp in edge.iter(f"{DI_NS}waypoint"):
            points.append(
                (
                    int(float(attr(wp, "x", "0"))),
                    int(float(attr(wp, "y", "0"))),
                )
            )
        if points:
            edges[ref] = points
    return edges


def find_diagram(root: ET.Element, process_id: str) -> ET.Element | None:
    for diagram in root.iter(f"{BPMNDI_NS}BPMNDiagram"):
        for plane in diagram.iter(f"{BPMNDI_NS}BPMNPlane"):
            if attr(plane, "bpmnElement") == process_id:
                return diagram
    diagrams = list(root.iter(f"{BPMNDI_NS}BPMNDiagram"))
    return diagrams[0] if diagrams else None


def lane_map(process: ET.Element) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for lane in process.iter(f"{BPMN_NS}lane"):
        lane_id = attr(lane, "id")
        for ref in lane.iter(f"{BPMN_NS}flowNodeRef"):
            if ref.text:
                mapping[ref.text.strip()] = lane_id
    return mapping


def flow_endpoints(process: ET.Element) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    outgoing: dict[str, list[str]] = {}
    incoming: dict[str, list[str]] = {}
    flows: list[tuple[str, str, str]] = []
    for elem in process:
        if local(elem.tag) != "sequenceFlow":
            continue
        fid = attr(elem, "id")
        src = attr(elem, "sourceRef")
        tgt = attr(elem, "targetRef")
        flows.append((fid, src, tgt))
        outgoing.setdefault(src, []).append(fid)
        incoming.setdefault(tgt, []).append(fid)
    return outgoing, incoming


def event_trigger(elem: ET.Element) -> str:
    for child in elem:
        name = local(child.tag)
        if name.endswith("EventDefinition"):
            if name == "timerEventDefinition":
                return "Timer"
            if name == "messageEventDefinition":
                return "Message"
            if name == "signalEventDefinition":
                return "Signal"
            if name == "errorEventDefinition":
                return "Error"
            if name == "terminateEventDefinition":
                return "Terminate"
    return "None"


def graphics_xml(
    element_id: str,
    bounds: dict[str, tuple[int, int, int, int]],
    lane_id: str | None = None,
) -> str:
    x, y, w, h = bounds.get(element_id, (160, 160, 120, 80))
    lane_attr = f' LaneId="{esc(lane_id)}"' if lane_id else ""
    return (
        "      <NodeGraphicsInfos>\n"
        f'        <NodeGraphicsInfo ToolId="BizAgi_Process_Modeler" Height="{h}" '
        f'Width="{w}" BorderColor="-16777216" FillColor="-1"{lane_attr}>\n'
        f'          <Coordinates XCoordinate="{x}" YCoordinate="{y}"/>\n'
        "        </NodeGraphicsInfo>\n"
        "      </NodeGraphicsInfos>\n"
    )


def connector_xml(flow_id: str, waypoints: dict[str, list[tuple[int, int]]]) -> str:
    points = waypoints.get(flow_id)
    if not points:
        return ""
    chunks = []
    for x, y in points:
        chunks.append(f'          <Coordinates XCoordinate="{x}" YCoordinate="{y}"/>')
    return (
        "      <ConnectorGraphicsInfos>\n"
        '        <ConnectorGraphicsInfo ToolId="BizAgi_Process_Modeler" '
        'BorderColor="-16777216">\n'
        f"{chr(10).join(chunks)}\n"
        "        </ConnectorGraphicsInfo>\n"
        "      </ConnectorGraphicsInfos>\n"
    )


def gateway_restriction(
    gateway_id: str,
    gtype: str,
    outgoing: dict[str, list[str]],
    incoming: dict[str, list[str]],
) -> str:
    out_count = len(outgoing.get(gateway_id, []))
    in_count = len(incoming.get(gateway_id, []))
    if out_count <= 1 and in_count <= 1:
        return ""
    parts = ["      <TransitionRestrictions>\n", "        <TransitionRestriction>\n"]
    if out_count > 1:
        refs = "".join(
            f'              <TransitionRef Id="{esc(fid)}"/>\n'
            for fid in outgoing.get(gateway_id, [])
        )
        parts.append(f'          <Split Type="{gtype}">\n')
        parts.append("            <TransitionRefs>\n")
        parts.append(refs)
        parts.append("            </TransitionRefs>\n")
        parts.append("          </Split>\n")
    if in_count > 1:
        parts.append(f'          <Join Type="{gtype}"/>\n')
    parts.append("        </TransitionRestriction>\n")
    parts.append("      </TransitionRestrictions>\n")
    return "".join(parts)


def activity_xml(
    elem: ET.Element,
    bounds: dict[str, tuple[int, int, int, int]],
    lanes: dict[str, str],
    outgoing: dict[str, list[str]],
    incoming: dict[str, list[str]],
) -> str:
    tag = local(elem.tag)
    aid = attr(elem, "id")
    name = attr(elem, "name", aid)
    lane_id = lanes.get(aid)
    body = [f'    <Activity Id="{esc(aid)}" Name="{esc(name)}">\n']

    if tag in EVENT_TAGS:
        body.append("      <Event>\n")
        if tag == "startEvent":
            trigger = event_trigger(elem)
            body.append(f'        <StartEvent Trigger="{esc(trigger)}"/>\n')
        elif tag == "endEvent":
            body.append("        <EndEvent/>\n")
        else:
            trigger = event_trigger(elem)
            body.append(f'        <IntermediateEvent Trigger="{esc(trigger)}"/>\n')
        body.append("      </Event>\n")
    elif tag in TASK_TAGS:
        body.append("      <Implementation>\n")
        body.append("        <Task/>\n")
        body.append("      </Implementation>\n")
    elif tag in GATEWAY_TAGS:
        gtype = GATEWAY_TYPES.get(tag, "XOR")
        marker = ' MarkerVisible="true"' if attr(elem, "gatewayDirection") else ""
        body.append(f'      <Route GatewayType="{gtype}"{marker}/>\n')
        body.append(
            gateway_restriction(aid, gtype, outgoing, incoming)
        )
    elif tag == "callActivity":
        called = attr(elem, "calledElement", aid)
        body.append("      <Implementation>\n")
        body.append(f'        <SubFlow Id="{esc(called)}" Execution="SYNCHR"/>\n')
        body.append("      </Implementation>\n")
    elif tag == "subProcess":
        body.append(
            f'      <BlockActivity ActivitySetId="ActivitySet_{esc(aid)}" View="COLLAPSED"/>\n'
        )
    else:
        body.append("      <Implementation>\n")
        body.append("        <No/>\n")
        body.append("      </Implementation>\n")

    body.append(graphics_xml(aid, bounds, lane_id))
    body.append(
        "      <ExtendedAttributes>\n"
        f'        <ExtendedAttribute Name="BPMNElement" Value="{esc(tag)}"/>\n'
        "      </ExtendedAttributes>\n"
    )
    body.append("    </Activity>\n")
    return "".join(body)


def collect_nodes(process: ET.Element) -> list[ET.Element]:
    nodes: list[ET.Element] = []
    for elem in process:
        tag = local(elem.tag)
        if tag in {"sequenceFlow", "laneSet", "dataObject", "dataObjectReference", "association"}:
            continue
        if tag == "subProcess":
            nodes.append(elem)
            continue
        if tag in EVENT_TAGS | TASK_TAGS | GATEWAY_TAGS | {"callActivity"}:
            nodes.append(elem)
    return nodes


def subprocess_internals(
    subprocess: ET.Element,
    bounds: dict[str, tuple[int, int, int, int]],
    waypoints: dict[str, list[tuple[int, int]]],
) -> tuple[str, str]:
    out_map, in_map = flow_endpoints(subprocess)
    lanes = lane_map(subprocess)
    activities = []
    transitions = []
    for node in collect_nodes(subprocess):
        if local(node.tag) == "subProcess":
            inner_act, inner_trans = subprocess_internals(node, bounds, waypoints)
            activities.append(inner_act)
            transitions.append(inner_trans)
        activities.append(
            activity_xml(node, bounds, lanes, out_map, in_map)
        )
    for flow in subprocess:
        if local(flow.tag) != "sequenceFlow":
            continue
        fid = attr(flow, "id")
        transitions.append(
            f'    <Transition Id="{esc(fid)}" From="{esc(attr(flow, "sourceRef"))}" '
            f'To="{esc(attr(flow, "targetRef"))}">\n'
            f"{connector_xml(fid, waypoints)}"
            "    </Transition>\n"
        )
    return "".join(activities), "".join(transitions)


def convert_process(
    process: ET.Element,
    diagram: ET.Element | None,
) -> tuple[str, str]:
    pid = attr(process, "id")
    pname = attr(process, "name", pid)
    bounds = parse_bounds(diagram)
    waypoints = parse_waypoints(diagram)
    out_map, in_map = flow_endpoints(process)
    lanes = lane_map(process)
    activity_sets: list[str] = []

    activities = []
    for node in collect_nodes(process):
        tag = local(node.tag)
        if tag == "subProcess":
            sid = attr(node, "id")
            inner_act, inner_trans = subprocess_internals(node, bounds, waypoints)
            activity_sets.append(
                f'  <ActivitySet Id="ActivitySet_{esc(sid)}" Name="{esc(attr(node, "name", sid))}">\n'
                "    <Activities>\n"
                f"{inner_act}"
                "    </Activities>\n"
                "    <Transitions>\n"
                f"{inner_trans}"
                "    </Transitions>\n"
                "  </ActivitySet>\n"
            )
        activities.append(activity_xml(node, bounds, lanes, out_map, in_map))

    transitions = []
    for flow in process:
        if local(flow.tag) != "sequenceFlow":
            continue
        fid = attr(flow, "id")
        transitions.append(
            f'    <Transition Id="{esc(fid)}" From="{esc(attr(flow, "sourceRef"))}" '
            f'To="{esc(attr(flow, "targetRef"))}">\n'
            f"{connector_xml(fid, waypoints)}"
            "    </Transition>\n"
        )

    pool_xml = ""
    if lanes:
        lane_entries = []
        for lane in process.iter(f"{BPMN_NS}lane"):
            lid = attr(lane, "id")
            lname = attr(lane, "name", lid)
            lane_entries.append(
                f'      <Lane Id="{esc(lid)}" Name="{esc(lname)}" '
                f'ParentPool="Pool_{esc(pid)}"/>\n'
            )
        pool_xml = (
            f'    <Pool Id="Pool_{esc(pid)}" Name="{esc(pname)}" '
            f'Process="{esc(pid)}" BoundaryVisible="false">\n'
            "      <Lanes>\n"
            f"{''.join(lane_entries)}"
            "      </Lanes>\n"
            "    </Pool>\n"
        )

    activity_sets_xml = ""
    if activity_sets:
        activity_sets_xml = (
            "    <ActivitySets>\n"
            f"{''.join(activity_sets)}"
            "    </ActivitySets>\n"
        )

    wf = (
        f'  <WorkflowProcess Id="{esc(pid)}" Name="{esc(pname)}">\n'
        "    <ProcessHeader/>\n"
        f"{activity_sets_xml}"
        "    <Activities>\n"
        f"{''.join(activities)}"
        "    </Activities>\n"
        "    <Transitions>\n"
        f"{''.join(transitions)}"
        "    </Transitions>\n"
        "  </WorkflowProcess>\n"
    )
    return wf, pool_xml


def convert_bpmn_file(bpmn_path: Path) -> str:
    tree = ET.parse(bpmn_path)
    root = tree.getroot()
    processes = list(root.iter(f"{BPMN_NS}process"))
    if not processes:
        raise ValueError(f"No bpmn:process found in {bpmn_path}")

    created = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    package_name = bpmn_path.stem
    workflow_chunks: list[str] = []
    pool_chunks: list[str] = []
    for process in processes:
        pid = attr(process, "id")
        diagram = find_diagram(root, pid)
        wf, pool = convert_process(process, diagram)
        workflow_chunks.append(wf)
        if pool:
            pool_chunks.append(pool)

    pools_xml = ""
    if pool_chunks:
        pools_xml = "  <Pools>\n" + "".join(pool_chunks) + "  </Pools>\n"

    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<Package xmlns="http://www.wfmc.org/2009/XPDL2.2" '
        f'Id="Package_{esc(package_name)}" Name="{esc(package_name)}">\n'
        "  <PackageHeader>\n"
        "    <XPDLVersion>2.2</XPDLVersion>\n"
        "    <Vendor>Industrial R&amp;D Practice BPMN Converter</Vendor>\n"
        f"    <Created>{created}</Created>\n"
        "    <Description>Converted from BPMN 2.0 for Bizagi Modeler import</Description>\n"
        "  </PackageHeader>\n"
        f"{pools_xml}"
        "  <WorkflowProcesses>\n"
        f"{''.join(workflow_chunks)}"
        "  </WorkflowProcesses>\n"
        "</Package>\n"
    )


def output_path_for(bpmn_path: Path, out_root: Path) -> Path:
    for source in DEFAULT_SOURCES:
        try:
            rel = bpmn_path.resolve().relative_to(source.resolve())
            return out_root / source.name / rel.with_suffix(".xpdl")
        except ValueError:
            continue
    return out_root / bpmn_path.with_suffix(".xpdl").name


def convert_path(path: Path, out_root: Path) -> list[Path]:
    written: list[Path] = []
    if path.is_file():
        targets = [path]
    else:
        targets = sorted(path.rglob("*.bpmn"))
    for bpmn_file in targets:
        xpdl = convert_bpmn_file(bpmn_file)
        out_file = output_path_for(bpmn_file, out_root)
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_text(xpdl, encoding="utf-8")
        written.append(out_file)
        message = f"Wrote {out_file}"
        try:
            print(message)
        except UnicodeEncodeError:
            print(message.encode("ascii", "replace").decode("ascii"))
    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Convert BPMN 2.0 XML to XPDL 2.2.")
    parser.add_argument(
        "paths",
        nargs="*",
        help="BPMN files or folders (default: Output/ and XML код/)",
    )
    parser.add_argument(
        "--out",
        default=str(DEFAULT_OUT),
        help=f"Output root folder (default: {DEFAULT_OUT})",
    )
    args = parser.parse_args(argv)
    out_root = Path(args.out)
    inputs = [Path(p) for p in args.paths] if args.paths else DEFAULT_SOURCES

    written: list[Path] = []
    for item in inputs:
        if not item.exists():
            print(f"Skip missing path: {item}", file=sys.stderr)
            continue
        written.extend(convert_path(item, out_root))

    if not written:
        print("No BPMN files converted.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

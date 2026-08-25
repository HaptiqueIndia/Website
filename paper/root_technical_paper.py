"""Canonical, evidence-aware content for the ROOT technical concept paper."""

DOCUMENT = {
    "title": "ROOT: A local architecture for room-level AC comfort",
    "subtitle": "Technical concept paper",
    "document_id": "ROOT-TCP-001",
    "revision": "D0.1",
    "publication_status": "Developer preview",
    "owner": "Haptique Electronics Pvt. Ltd.",
    "technical_reviewer": "Not yet assigned",
    "issue_date": "25 August 2026",
    "last_reviewed": "25 August 2026",
    "evidence_cutoff": "25 August 2026",
    "hardware_revision": "Not yet assigned",
    "firmware_revision": "Not yet assigned",
}

EVIDENCE_STATUSES = (
    "Cited background",
    "Implemented prototype behavior",
    "Hypothesis / design target",
    "Planned evaluation",
)

FORBIDDEN_COPY = (
    "acceleration award", "affiliated with panasonic", "patent pending",
    "breathing sense", "zero outages", "perfect coverage",
    "universal compatibility", "fully-tested", "100% local",
)

SECTIONS = (
    {
        "id": "abstract",
        "number": "Abstract",
        "title": "A proposed local architecture for room-level AC comfort.",
        "paragraphs": (
            "ROOT is a proposed controller for IR-operated split air conditioners. Its design thesis is to sense conditions closer to an occupied location, make bounded control decisions on the device, and transmit adjustments through the AC's existing infrared interface.",
            "This paper describes the intended architecture, its control and privacy boundaries, and the evaluation methods required before product-performance statements can be made. It reports no measured product-performance result. All unmeasured ROOT behavior is classified as a hypothesis, design target, or planned evaluation.",
        ),
    },
    {
        "id": "room-level-problem",
        "number": "1",
        "title": "The occupied part of a room can differ from the return-air reference.",
        "paragraphs": (
            "Split air conditioners typically regulate from a temperature reference near the indoor unit. Airflow, heat loads, room geometry, and occupant location can create non-uniform conditions that a single reference does not fully describe.",
            "ROOT's design hypothesis is narrower: a sensor placed near a bed, couch, or desk may provide a more relevant control input for that location. The magnitude and usefulness of any difference remain dependent on the room and must be measured.",
        ),
    },
    {
        "id": "architecture",
        "number": "2",
        "title": "A four-stage loop with a deliberately small control boundary.",
        "paragraphs": (
            "The intended loop is: sense the room; estimate occupancy or context; decide locally; and transmit an infrared adjustment. Temperature, humidity, and a bounded presence signal are proposed inputs near the intended occupied location.",
            "The proposed decision path uses bounded setpoints, bounded command rates, manual override, and a neutral fallback. An emitted infrared command is not treated as confirmed AC state. Conceptual architecture diagrams are not measured results.",
        ),
    },
    {
        "id": "connectivity",
        "number": "3",
        "title": "Local control is a scoped pathway, not a blanket privacy or uptime claim.",
        "paragraphs": (
            "Bluetooth is a proposed configuration pathway. The intended remote-learning flow records supported IR commands from the existing AC remote; configuration storage, sensing, decision, and IR transmission are proposed device pathways. Exact permissions, pairing authorization, retained identifiers, storage, retention, deletion, sharing, and reset behavior require a reviewed data-flow design.",
            "Offline operation must be evaluated after setup through sensing, decision, command, reboot, and reconnection scenarios. Bluetooth received signal strength varies with orientation, obstruction, radio conditions, and implementation; it is a coarse input and must not be the sole basis for a safety-relevant or irreversible action.",
        ),
    },
    {
        "id": "sensing",
        "number": "4",
        "title": "Sensing and infrared are system elements awaiting integrated validation.",
        "paragraphs": (
            "Temperature and humidity are proposed control inputs; part specifications and display resolution do not establish integrated system accuracy. Presence sensing is limited to room-control context and is not health or vital-sign monitoring.",
            "IR learning is intended to record supported commands without implying broad compatibility. Infrared transmission reach depends on orientation, distance, line of sight, surfaces, emitter configuration, and the receiving AC. Illustrative product imagery is not evidence of final components, layout, construction, or production readiness.",
        ),
    },
    {
        "id": "placement",
        "number": "5",
        "title": "Placement changes what the device can sense and reach.",
        "paragraphs": (
            "Tabletop, nightstand, couch-side, desk-side, and wall-mounted arrangements are placement concepts, not equivalent operating modes. Each changes sampled air, exposure to drafts or heat sources, sensor obstruction, mounting stability, occupant proximity, and the IR path to the AC.",
            "Placement guidance must be tied to tested room and AC configurations. Users should retain access to manual AC controls when the recommended position cannot provide a reliable sensing or transmission path.",
        ),
    },
    {
        "id": "evaluation",
        "number": "6",
        "title": "Report protocols before results.",
        "paragraphs": (
            "Every planned evaluation identifies the prototype and firmware revision, room or bench conditions, comparator and ground truth, sample interval, repeated trials, primary and secondary outcomes, acceptance criterion fixed before testing, exclusions and missing-data handling, uncertainty, and retained evidence artifact.",
            "Future reports must include trial counts, negative results, protocol deviations, raw and derived data location, and analysis version. A simulator output is not a measured result.",
        ),
    },
    {
        "id": "limitations",
        "number": "7",
        "title": "A comfort controller with explicit limits.",
        "paragraphs": (
            "ROOT is intended for general room-comfort control. It is not a medical device and is not intended to diagnose, prevent, monitor, predict, mitigate, or treat disease, injury, disability, a physiological condition, sleep, or a vital sign.",
            "ROOT is not a safety-critical, emergency, or life-support controller. Users must retain the original AC remote and access to the AC's manual controls. Bounded setpoints, bounded command rates, visible fault indication, manual override, and a neutral fallback remain design targets until implemented and tested.",
            "Validation must cover sensor faults, stale or out-of-range inputs, proximity loss, ambiguous or unsupported IR state, blocked line of sight, AC non-response, power interruption and restart, conflicting occupant preferences, mounting failure, and optional-connectivity loss. Compatibility and performance depend on AC hardware, room geometry, placement, obstruction, environmental conditions, power, firmware, and operating mode.",
        ),
    },
    {
        "id": "company",
        "number": "8",
        "title": "Haptique Electronics is developing ROOT.",
        "paragraphs": (
            "Haptique Electronics Pvt. Ltd. is the company developing ROOT as a room-comfort product concept. ROOT is a product and brand, not a separate legal entity.",
            "This revision intentionally omits third-party recognition and intellectual-property status. Those disclosures require verified identity, filing, scope, and approval records before inclusion. Developer contact: info@get-root.in.",
        ),
    },
    {
        "id": "references",
        "number": "9",
        "title": "References.",
        "paragraphs": (
            "The cited background and Bluetooth measurement context are identified in the numbered reference register below.",
        ),
    },
    {
        "id": "revision-history",
        "number": "10",
        "title": "Revision history.",
        "paragraphs": (
            "D0.1, issued 25 August 2026 by Haptique Electronics Pvt. Ltd.; reviewer: Not yet assigned; evidence cutoff: 25 August 2026. Initial developer-preview concept paper. No prototype performance result is reported.",
        ),
    },
)

CLAIMS = (
    {
        "id": "CB-01", "status": "Cited background",
        "scope": "HVAC background and design motivation", "revision": "Not applicable",
        "evidence_id": "REF-01", "evidence_date": "2026",
        "wording": "Non-uniform conditions can arise in split-AC rooms, so a single return-air reference may not fully describe conditions near an occupant.",
    },
    {
        "id": "HT-01", "status": "Hypothesis / design target",
        "scope": "Proposed four-stage room-control loop", "revision": "Target revision not yet assigned",
        "evidence_id": "DESIGN-REVIEW-2026-08-25", "evidence_date": "25 August 2026",
        "wording": "ROOT is designed to sense room context, decide locally within bounded controls, and transmit a learned IR adjustment.",
    },
    {
        "id": "HT-02", "status": "Hypothesis / design target",
        "scope": "Proposed setup and local-control boundary", "revision": "Target revision not yet assigned",
        "evidence_id": "REF-02; DESIGN-REVIEW-2026-08-25", "evidence_date": "25 August 2026",
        "wording": "Bluetooth is a proposed setup or coarse-proximity pathway, while the intended core sensing, decision, and IR paths operate on the device after configuration.",
    },
    {
        "id": "HT-03", "status": "Hypothesis / design target",
        "scope": "Proposed sensing and infrared interface", "revision": "Target revision not yet assigned",
        "evidence_id": "DESIGN-REVIEW-2026-08-25", "evidence_date": "25 August 2026",
        "wording": "Temperature, humidity, presence sensing, IR learning, and IR transmission require integrated validation before accuracy, reach, or compatibility claims are made.",
    },
    {
        "id": "HT-04", "status": "Hypothesis / design target",
        "scope": "Placement concepts", "revision": "Target revision not yet assigned",
        "evidence_id": "DESIGN-REVIEW-2026-08-25", "evidence_date": "25 August 2026",
        "wording": "Placement affects sampled conditions, obstruction, airflow exposure, line of sight, IR reach, mounting stability, and presence-detection behavior.",
    },
    {
        "id": "PE-01", "status": "Planned evaluation",
        "scope": "Climate sensing", "revision": "Target revision not yet assigned",
        "evidence_id": "PROTOCOL-01", "evidence_date": "25 August 2026",
        "wording": "Co-locate ROOT with a traceable reference logger and report bias, mean absolute error, repeatability, sampling interval, stabilization time, and uncertainty.",
    },
    {
        "id": "PE-02", "status": "Planned evaluation",
        "scope": "Presence sensing", "revision": "Target revision not yet assigned",
        "evidence_id": "PROTOCOL-02", "evidence_date": "25 August 2026",
        "wording": "Compare presence detections with timestamped ground truth across occupied, unoccupied, stationary, moving, obstructed, placement, and false-trigger scenarios.",
    },
    {
        "id": "PE-03", "status": "Planned evaluation",
        "scope": "IR interoperability", "revision": "Target revision not yet assigned",
        "evidence_id": "PROTOCOL-03", "evidence_date": "25 August 2026",
        "wording": "Test a declared stratified sample of AC brands, models, and commands over repeated trials, distances, angles, and line-of-sight conditions, reporting model-level successes and failures.",
    },
    {
        "id": "PE-04", "status": "Planned evaluation",
        "scope": "Offline control", "revision": "Target revision not yet assigned",
        "evidence_id": "PROTOCOL-04", "evidence_date": "25 August 2026",
        "wording": "Disable Wi-Fi and internet after setup, then exercise sensing, decisions, commands, reboot, and reconnection for a stated duration.",
    },
    {
        "id": "PE-05", "status": "Planned evaluation",
        "scope": "Setup", "revision": "Target revision not yet assigned",
        "evidence_id": "PROTOCOL-05", "evidence_date": "25 August 2026",
        "wording": "Observe first-time users completing a defined setup flow and report completion rate, timing distributions, assistance, retries, and failure reasons.",
    },
    {
        "id": "PE-06", "status": "Planned evaluation",
        "scope": "Power behavior", "revision": "Target revision not yet assigned",
        "evidence_id": "PROTOCOL-06", "evidence_date": "25 August 2026",
        "wording": "Measure nominal and peak draw, supported input conditions, brownout and restart behavior, and recovery state using declared equipment.",
    },
    {
        "id": "PE-07", "status": "Planned evaluation",
        "scope": "Room comfort stability", "revision": "Target revision not yet assigned",
        "evidence_id": "PROTOCOL-07", "evidence_date": "25 August 2026",
        "wording": "Use a randomized or counterbalanced baseline-versus-ROOT comparison with recorded conditions and predefined occupant-zone deviation, overshoot, cycling, and humidity outcomes.",
    },
)

REFERENCES = (
    {
        "id": "REF-01",
        "title": "Human thermal responses to non-uniform cooling from intermittently operated split air conditioners",
        "publisher": "Building and Environment",
        "publication_date": "2026",
        "url": "https://doi.org/10.1016/j.buildenv.2026.114379",
        "access_date": "25 August 2026",
    },
    {
        "id": "REF-02",
        "organization": "Bluetooth SIG",
        "title": "Bluetooth Low Energy Primer",
        "publisher": "Bluetooth SIG",
        "publication_date": "Not dated",
        "url": "https://www.bluetooth.com/bluetooth-le-primer/",
        "access_date": "25 August 2026",
    },
)

PROTOCOLS = (
    {"id": "PROTOCOL-01", "claim_id": "PE-01", "title": "Climate sensing", "primary_outcomes": ("bias", "mean absolute error", "repeatability", "measurement uncertainty"), "acceptance_criterion": "Fixed before testing"},
    {"id": "PROTOCOL-02", "claim_id": "PE-02", "title": "Presence sensing", "primary_outcomes": ("sensitivity", "specificity or false-positive rate", "response latency"), "acceptance_criterion": "Fixed before testing"},
    {"id": "PROTOCOL-03", "claim_id": "PE-03", "title": "IR interoperability", "primary_outcomes": ("model-level successes", "model-level failures"), "acceptance_criterion": "Fixed before testing"},
    {"id": "PROTOCOL-04", "claim_id": "PE-04", "title": "Offline control", "primary_outcomes": ("sensing, decision, command, reboot, and reconnection behavior",), "acceptance_criterion": "Fixed before testing"},
    {"id": "PROTOCOL-05", "claim_id": "PE-05", "title": "Setup", "primary_outcomes": ("completion rate", "median and range or interquartile range", "assistance", "retries", "failure reasons"), "acceptance_criterion": "Fixed before testing"},
    {"id": "PROTOCOL-06", "claim_id": "PE-06", "title": "Power behavior", "primary_outcomes": ("nominal draw", "peak draw", "brownout and restart behavior", "recovery state"), "acceptance_criterion": "Fixed before testing"},
    {"id": "PROTOCOL-07", "claim_id": "PE-07", "title": "Room comfort stability", "primary_outcomes": ("occupant-zone deviation", "overshoot", "cycling", "humidity"), "acceptance_criterion": "Fixed before testing"},
)

REVISION_HISTORY = (
    {
        "revision": "D0.1", "issue_date": "25 August 2026",
        "owner": "Haptique Electronics Pvt. Ltd.", "reviewer": "Not yet assigned",
        "evidence_cutoff": "25 August 2026",
        "summary": "Initial developer-preview concept paper. No prototype performance result is reported.",
    },
)

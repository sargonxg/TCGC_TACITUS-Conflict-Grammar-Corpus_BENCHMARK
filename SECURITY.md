# Security Policy

## Supported status

TCGC is an alpha research benchmark and corpus. Security-sensitive fixes should target the default branch. The project does not currently promise long-term support for earlier commits, schemas, corpus versions, or experimental adapters.

## Reporting a vulnerability

Report suspected vulnerabilities privately to **hello@tacitus.me**. Do not open a public issue containing exploit details, credentials, private prediction files, unpublished benchmark data, or personal information.

Useful reports identify:

- the affected commit and component;
- the execution path or adapter involved;
- reproduction steps;
- the likely impact on users, data, scoring, or supply-chain integrity; and
- any immediate containment measure.

A report will be acknowledged when reviewed. No response-time or bounty commitment is currently offered.

## Benchmark and data integrity

Security reports may include, among other issues:

- arbitrary code execution through adapters or runner interfaces;
- unsafe deserialization or path traversal;
- credential exposure in API-backed experiments;
- malicious corpus items or generated artifacts;
- dependency or workflow compromise;
- leakage of hidden annotations or evaluation material; and
- scoring behavior that can be manipulated outside the documented prediction contract.

Do not commit provider keys, unpublished predictions, confidential corpora, private annotations, or generated credentials. Use the opt-in API paths only after reviewing their data flow and cost behavior.

## Disclosure

Allow reasonable time for investigation and remediation before public disclosure. Maintainers may request coordinated disclosure when downstream users or published results could remain affected.

from pathlib import Path
from xml.sax.saxutils import escape
import zipfile


OUTPUT = Path(r"C:\Users\kumar.gn\HCLProjects\BusinessProcess\CUNB Weekly Data Request - Business Version.docx")


def p(text, style=None):
    style_xml = f"<w:pPr><w:pStyle w:val=\"{style}\"/></w:pPr>" if style else ""
    return (
        "<w:p>"
        f"{style_xml}"
        "<w:r><w:t xml:space=\"preserve\">"
        f"{escape(text)}"
        "</w:t></w:r>"
        "</w:p>"
    )


def tc(text, width, header=False):
    shade = '<w:shd w:fill="D9EAF7"/>' if header else ""
    bold_start = "<w:b/>" if header else ""
    return (
        "<w:tc>"
        f"<w:tcPr><w:tcW w:w=\"{width}\" w:type=\"dxa\"/>{shade}</w:tcPr>"
        "<w:p><w:r><w:rPr>"
        f"{bold_start}"
        "<w:sz w:val=\"20\"/>"
        "</w:rPr><w:t xml:space=\"preserve\">"
        f"{escape(text)}"
        "</w:t></w:r></w:p>"
        "</w:tc>"
    )


def tr(cells, header=False):
    return "<w:tr>" + "".join(tc(text, width, header) for text, width in cells) + "</w:tr>"


def table(headers, rows, widths):
    tbl_pr = (
        "<w:tblPr>"
        "<w:tblStyle w:val=\"TableGrid\"/>"
        "<w:tblW w:w=\"0\" w:type=\"auto\"/>"
        "<w:tblBorders>"
        "<w:top w:val=\"single\" w:sz=\"4\" w:space=\"0\" w:color=\"B7C3CC\"/>"
        "<w:left w:val=\"single\" w:sz=\"4\" w:space=\"0\" w:color=\"B7C3CC\"/>"
        "<w:bottom w:val=\"single\" w:sz=\"4\" w:space=\"0\" w:color=\"B7C3CC\"/>"
        "<w:right w:val=\"single\" w:sz=\"4\" w:space=\"0\" w:color=\"B7C3CC\"/>"
        "<w:insideH w:val=\"single\" w:sz=\"4\" w:space=\"0\" w:color=\"D5DDE3\"/>"
        "<w:insideV w:val=\"single\" w:sz=\"4\" w:space=\"0\" w:color=\"D5DDE3\"/>"
        "</w:tblBorders>"
        "</w:tblPr>"
    )
    grid = "<w:tblGrid>" + "".join(f'<w:gridCol w:w="{w}"/>' for w in widths) + "</w:tblGrid>"
    header_row = tr(list(zip(headers, widths)), header=True)
    body_rows = "".join(tr(list(zip(row, widths))) for row in rows)
    return "<w:tbl>" + tbl_pr + grid + header_row + body_rows + "</w:tbl>"


title = p("CUNB Weekly Data Request", "Title")
subtitle = p(
    "Business-facing data request to recreate the weekly CUNB analysis, movement views, billing plan views, and management summaries from CUNB-2 Mar'26 V.1.xlsx.",
    "Subtitle",
)

sections = []
sections.append(p("1. Objective", "Heading1"))
sections.append(
    p(
        "The goal is to reproduce the CUNB analysis week on week at L3, account, and resource level, including billed-to-unbilled movements, unbilled-to-billed recoveries, billing plan tracking, no-plan tracking, and root-cause summaries."
    )
)
sections.append(
    p(
        "To do that reliably, the required input is a weekly resource-level snapshot. Summary counts by account and L3 alone are not sufficient for the full analysis."
    )
)

sections.append(p("2. Weekly File Expected", "Heading1"))
sections.append(
    table(
        ["Item", "Business Requirement"],
        [
            ["Frequency", "One file every week"],
            ["Granularity", "One row per resource-assignment per snapshot date"],
            ["Recommended format", "Excel or CSV with identical schema every week"],
            ["Date convention", "Consistent week start or week end date across all files"],
            ["If a resource is split", "Create separate rows by assignment with correct FTE or allocation split"],
        ],
        [2600, 6200],
    )
)

sections.append(p("3. Mandatory Fields", "Heading1"))
sections.append(
    table(
        ["Category", "Mandatory Fields", "Why Needed"],
        [
            ["Resource Identity", "Employee Code, Employee Name, Personal ID", "Needed to track the same person week on week"],
            ["Snapshot Details", "Snapshot Date or Calendar Day", "Needed for weekly comparison and trend creation"],
            ["Assignment", "Project Code, Project Name, Customer, Project L2, Project L3, Project L4", "Needed for L2/L3/L4 and account analysis"],
            ["Capacity", "FTE, Allocation Percentage", "Needed to aggregate movement and total CUNB correctly"],
            ["Billing State", "Billing Status, Billing Status 2, Expected Bill Date or BSD", "Needed to classify billed, unbilled, billing planned, and no-plan cases"],
            ["Movement Context", "Reason Code, Current Status, Category, Category2", "Needed to explain why a case moved or remained unbilled"],
            ["Resource Type", "Fresher or FCL or Lateral, Band, Sub-Band, Date of Joining", "Needed for freshers, laterals, and experience-based summaries"],
            ["Location Mix", "Onsite or Offshore or Nearshore, Country, Location or Personnel Subarea", "Needed for delivery and deployment views"],
            ["Ownership", "Reporting Manager, PM Name, HR L3 Head, Project L3 Head, Project L4 Head", "Needed for owner-based reviews and action tracking"],
        ],
        [1800, 4100, 2900],
    )
)

sections.append(p("4. Week-on-Week Comparison Requirement", "Heading1"))
sections.append(
    table(
        ["Required Option", "Details"],
        [
            ["Preferred option", "Provide one full snapshot file every week using the same schema"],
            ["Alternative option", "Provide current-week data with prior-week billing and project state already attached"],
            ["Prior-week fields if attached", "Prior Week Billing Status, Prior Week Project Code, Prior Week Project Name, Prior Week Project L2, Prior Week Project L3, Prior Week Project L4, Prior Week FTE, Prior Week Expected Bill Date, Prior Week Reason Code"],
        ],
        [2500, 6300],
    )
)

sections.append(p("5. What This Enables", "Heading1"))
sections.append(
    table(
        ["Analysis Output", "Can Be Produced If Weekly Resource-Level Data Is Provided"],
        [
            ["Movement views", "Billed to Unbilled, Unbilled to Billed, New Added, Moved Out, Stayed Unbilled, Stayed Billed"],
            ["Commercial views", "Billing Plan by month, No Plan cases, Billing Plan dropped, BSD changes, future-dated billing"],
            ["Leadership views", "L3 summary, account summary, weekly trend charts, top contributors, management reviews"],
            ["Operational views", "Root-cause summaries, freshers and laterals views, owner-led action tracking, account-L3 hotspot analysis"],
            ["Resource detail views", "Named resource lists behind each movement bucket for follow-up and auditability"],
        ],
        [2500, 6300],
    )
)

sections.append(p("6. What Summary Counts Alone Can And Cannot Do", "Heading1"))
sections.append(
    table(
        ["If Only Weekly Billed and Unbilled Counts Are Shared", "Possible", "Not Possible Reliably"],
        [
            ["Account and L3 totals", "Trend charts, billed versus unbilled shifts, concentration analysis", "Named resource movement lists"],
            ["High-level movement story", "Top improving and deteriorating accounts or L3s", "Exact billed-to-unbilled and unbilled-to-billed classification by resource"],
            ["Business reporting", "Executive summaries and directional charts", "Root-cause analysis, billing plan detail, no-plan reason splits, fresher and investment views"],
        ],
        [2500, 2600, 3700],
    )
)

sections.append(p("7. Optional But Valuable Fields", "Heading1"))
sections.append(
    table(
        ["Optional Field Group", "Examples", "Value Added"],
        [
            ["Commercial workflow", "Billing Planned flag, Planned Billing Month, Customer Confirmation Status, SOW Status, RAS Status, Billing Plan Confidence", "Improves plan-versus-risk analysis"],
            ["Organization hierarchy", "HR L1 to L4, HR Heads, Project L1 to L4 Heads", "Improves accountability and review routing"],
            ["Project metadata", "Project Role, Skill, Skill Group, Capability Manager, Project Category, Project Nature, Archetype, Mode", "Improves root-cause and deployment analysis"],
            ["Special summaries", "Investment Approved flag, Investment Approved By, Investment Start Date, Investment End Date, Code Type C or E or Y, WBS Code, Diva or gender flag", "Enables investment, E/Y/C code, and diversity-based summaries"],
        ],
        [2100, 3300, 3400],
    )
)

sections.append(p("8. Recommended Weekly File Naming Standard", "Heading1"))
sections.append(
    table(
        ["Example", "Meaning"],
        [
            ["2026-02-09_snapshot.xlsx", "Weekly snapshot for week of February 9, 2026"],
            ["2026-02-16_snapshot.xlsx", "Weekly snapshot for week of February 16, 2026"],
            ["2026-02-23_snapshot.xlsx", "Weekly snapshot for week of February 23, 2026"],
            ["2026-03-02_snapshot.xlsx", "Weekly snapshot for week of March 2, 2026"],
        ],
        [3400, 5400],
    )
)

sections.append(p("9. Explicit Ask To The Data Team", "Heading1"))
sections.append(
    table(
        ["Ask", "Details"],
        [
            ["Weekly file delivery", "Please share one weekly resource-level snapshot file with a stable schema"],
            ["Minimum mandatory columns", "Please include all fields listed in the Mandatory Fields section"],
            ["Comparison support", "Please either share prior-week snapshots as separate files or attach prior-week state in the current file"],
            ["Data quality", "Please keep employee identifiers stable, FTE numeric, and dates standardized"],
            ["Scope control", "Please confirm whether the file includes only in-scope CUNB population or all assignment records with status"],
        ],
        [2500, 6300],
    )
)

sections.append(p("10. Bottom Line", "Heading1"))
sections.append(
    p(
        "To recreate the workbook properly week on week, the business needs full weekly resource-level snapshots rather than only summarized billed and unbilled totals. This is the minimum requirement to produce reliable movement analysis, billing plan views, no-plan views, and owner-led operational reporting."
    )
)


document_xml = (
    "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>"
    "<w:document xmlns:wpc=\"http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas\" "
    "xmlns:mc=\"http://schemas.openxmlformats.org/markup-compatibility/2006\" "
    "xmlns:o=\"urn:schemas-microsoft-com:office:office\" "
    "xmlns:r=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships\" "
    "xmlns:m=\"http://schemas.openxmlformats.org/officeDocument/2006/math\" "
    "xmlns:v=\"urn:schemas-microsoft-com:vml\" "
    "xmlns:wp14=\"http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing\" "
    "xmlns:wp=\"http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing\" "
    "xmlns:w10=\"urn:schemas-microsoft-com:office:word\" "
    "xmlns:w=\"http://schemas.openxmlformats.org/wordprocessingml/2006/main\" "
    "xmlns:w14=\"http://schemas.microsoft.com/office/word/2010/wordml\" "
    "xmlns:w15=\"http://schemas.microsoft.com/office/word/2012/wordml\" "
    "xmlns:wpg=\"http://schemas.microsoft.com/office/word/2010/wordprocessingGroup\" "
    "xmlns:wpi=\"http://schemas.microsoft.com/office/word/2010/wordprocessingInk\" "
    "xmlns:wne=\"http://schemas.microsoft.com/office/word/2006/wordml\" "
    "xmlns:wps=\"http://schemas.microsoft.com/office/word/2010/wordprocessingShape\" "
    "mc:Ignorable=\"w14 w15 wp14\">"
    "<w:body>"
    + title
    + subtitle
    + "".join(sections)
    + (
        "<w:sectPr>"
        "<w:pgSz w:w=\"12240\" w:h=\"15840\"/>"
        "<w:pgMar w:top=\"1080\" w:right=\"1080\" w:bottom=\"1080\" w:left=\"1080\" w:header=\"708\" w:footer=\"708\" w:gutter=\"0\"/>"
        "<w:cols w:space=\"708\"/>"
        "<w:docGrid w:linePitch=\"360\"/>"
        "</w:sectPr>"
        "</w:body></w:document>"
    )
)

content_types_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>
"""

rels_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>
"""

document_rels_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>
"""

styles_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:qFormat/>
    <w:rPr><w:sz w:val="20"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/>
    <w:basedOn w:val="Normal"/>
    <w:qFormat/>
    <w:rPr><w:b/><w:sz w:val="34"/><w:color w:val="1F2933"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Subtitle">
    <w:name w:val="Subtitle"/>
    <w:basedOn w:val="Normal"/>
    <w:qFormat/>
    <w:rPr><w:sz w:val="20"/><w:color w:val="5C636A"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:basedOn w:val="Normal"/>
    <w:qFormat/>
    <w:rPr><w:b/><w:sz w:val="24"/><w:color w:val="1565C0"/></w:rPr>
  </w:style>
</w:styles>
"""

core_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
 xmlns:dc="http://purl.org/dc/elements/1.1/"
 xmlns:dcterms="http://purl.org/dc/terms/"
 xmlns:dcmitype="http://purl.org/dc/dcmitype/"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>CUNB Weekly Data Request - Business Version</dc:title>
  <dc:creator>Codex</dc:creator>
  <cp:lastModifiedBy>Codex</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">2026-03-08T00:00:00Z</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">2026-03-08T00:00:00Z</dcterms:modified>
</cp:coreProperties>
"""

app_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
 xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Codex</Application>
</Properties>
"""


with zipfile.ZipFile(OUTPUT, "w", compression=zipfile.ZIP_DEFLATED) as docx:
    docx.writestr("[Content_Types].xml", content_types_xml)
    docx.writestr("_rels/.rels", rels_xml)
    docx.writestr("word/document.xml", document_xml)
    docx.writestr("word/_rels/document.xml.rels", document_rels_xml)
    docx.writestr("word/styles.xml", styles_xml)
    docx.writestr("docProps/core.xml", core_xml)
    docx.writestr("docProps/app.xml", app_xml)

print(OUTPUT)

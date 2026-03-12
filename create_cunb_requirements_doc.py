from pathlib import Path
from xml.sax.saxutils import escape
import zipfile


OUTPUT = Path(r"C:\Users\kumar.gn\HCLProjects\BusinessProcess\CUNB Weekly Data Requirements and Asks.docx")
TITLE = "CUNB Weekly Data Requirements and Asks"

SECTIONS = [
    (
        "Purpose",
        [
            "This document lists what is required to recreate the detailed analysis in CUNB-2 Mar'26 V.1.xlsx on a week-on-week basis.",
            "Resource-level billed and unbilled counts by account and L3 are not enough by themselves for the full workbook. They are sufficient for basic trend views, but not for movement classification, billing-plan analysis, root-cause splits, or the detailed operational tabs.",
        ],
    ),
    (
        "Minimum Weekly Grain",
        [
            "Each row should represent one resource-assignment snapshot for a given week.",
            "If one employee is split across multiple assignments, each assignment should appear as a separate row with its own FTE or allocation percentage.",
        ],
    ),
    (
        "Core Weekly Fields Required",
        [
            "Snapshot Date or Calendar Day",
            "Employee Code",
            "Employee Name",
            "Personal ID",
            "FTE",
            "Allocation Percentage",
            "Billing Status",
            "Account or Customer",
            "Project Code",
            "Project Name",
            "Project L2",
            "Project L3",
            "Project L4",
            "Assignment Start Date",
            "Assignment End Date",
            "Expected Bill Date or BSD",
            "Current Week Category",
            "Reason Code",
        ],
    ),
    (
        "Week-on-Week Comparison Fields",
        [
            "To rebuild movement tabs such as Got Billed, Billed to Unbilled, Week on Week Summary, and JFM Weekly Walk, I need either two full weekly snapshots or the prior-week state carried in the current extract.",
            "Required prior-week fields are: Prior Week Billing Status, Prior Week Project Code, Prior Week Project Name, Prior Week Project L2, Prior Week Project L3, Prior Week Project L4, Prior Week FTE, Prior Week Expected Bill Date, and Prior Week Reason Code.",
        ],
    ),
    (
        "Movement Classification Inputs",
        [
            "To classify week-on-week movement, I need enough information to identify the following buckets: Unbilled to Billed, Billed to Unbilled, Stayed Unbilled, Stayed Billed, Moved Out, New Added, Partial Billed to Unbilled, Unbilled VDU to CU, Billing Plan Got Dropped, BSD Changed, BSD Changed for Future Date, Back-dated Billing, and RAS Initiated or Corrected.",
            "This requires current and prior billing status, current and prior project mapping, current and prior expected bill date, movement reason, and whether the person entered or exited scope.",
        ],
    ),
    (
        "Commercial and Billing Plan Inputs",
        [
            "Billing Month",
            "Billing Planned flag",
            "Planned Billing Month",
            "Expected Bill Date",
            "Customer Confirmation Status",
            "SOW Status",
            "RAS Status",
            "Billing Plan Confidence such as Confirmed, Tentative, or Pending",
            "Billing Status 2 such as Billing Planned or No Billing Planned",
        ],
    ),
    (
        "Resource Segmentation Inputs",
        [
            "Fresher, FCL, or Lateral",
            "Fresher Flag",
            "Band",
            "Sub-Band",
            "Date of Joining",
            "Employee Type",
            "Onsite, Offshore, or Nearshore classification",
            "Country",
            "Location or Personnel Subarea",
            "Project Component",
        ],
    ),
    (
        "Organization and Ownership Inputs",
        [
            "HR L1, HR L2, HR L3, and HR L4",
            "HR L1 Head, HR L2 Head, HR L3 Head, and HR L4 Head",
            "Project L1 Head, Project L2 Head, Project L3 Head, and Project L4 Head",
            "PM Code and PM Name",
            "Manager Code and Reporting Manager",
        ],
    ),
    (
        "Operational Detail Inputs",
        [
            "Project Role",
            "Skill and Skill Group",
            "Capability Manager",
            "Project Category",
            "Project Nature or Archetype",
            "Mode and Group Description",
            "Rex months or years if that logic is used internally",
            "AAFD and TSS flags if they influence treatment",
            "Current Status",
            "Detailed Reason",
            "Category",
            "Category2",
        ],
    ),
    (
        "Special Inputs Needed for All Workbook Tabs",
        [
            "To support tabs such as Approved Investment, Investment Summary, Freshers Summary, Divas Summary, and E and Y Code, I would also need: Investment Approved flag, Investment Approved By, Investment Start Date, Investment End Date, Code Type such as C, E, or Y, WBS Code, Company Code, Company Name, CWL or Plant information, and any Diva or gender flag if the summary depends on it.",
        ],
    ),
    (
        "Explicit Weekly Ask",
        [
            "For every weekly file, I need: Resource identity fields, assignment fields, billing state fields, reason and actionability fields, resource segmentation fields, ownership fields, and either prior-week reference fields or the full prior-week extract in the same schema.",
            "At minimum, each weekly file should include: Employee Code, Employee Name, Personal ID, Snapshot Date, Project Code, Project Name, Customer, Project L2, Project L3, Project L4, FTE, Allocation Percentage, Billing Status, Billing Status 2, Expected Bill Date or BSD, Billing Month, Billing Planned flag, Planned Billing Month, RAS Status, SOW Status, Customer Approval Status, Reason Code, Detailed Reason, Category, Category2, Current Status, Fresher or FCL or Lateral, Band, Sub-Band, Date of Joining, Onsite or Offshore or Nearshore classification, Country, Employee Type, Reporting Manager, PM Name, HR L3 Head, Project L3 Head, and Project L4 Head.",
        ],
    ),
    (
        "How Many Weeks Are Needed",
        [
            "For basic movement analysis, I need at least two consecutive weekly snapshots.",
            "To reproduce the trend sheets and historical walk in the workbook, I need all weekly snapshots across the analysis period, ideally using a consistent week-ending or week-starting date convention.",
        ],
    ),
    (
        "What Can Be Produced From Only Billed and Unbilled Counts",
        [
            "If I receive only week, account, L3, billed count or billed FTE, and unbilled count or unbilled FTE, I can create trend charts, L3 and account movement summaries, billed versus unbilled shifts, concentration analysis, and top deteriorating or improving accounts and L3s.",
            "I cannot reliably create detailed resource lists for Got Billed or Billed to Unbilled, root-cause breakdowns, no-plan reason splits, billing-plan month analysis, freshers or divas or investment summaries, or the detailed actionability classifications.",
        ],
    ),
    (
        "Best Input Format",
        [
            "Best case is one Excel or CSV file per week, with the same schema every week, one row per resource-assignment, numeric FTE, and normalized dates.",
            "Recommended naming pattern: 2026-02-09_snapshot.xlsx, 2026-02-16_snapshot.xlsx, 2026-02-23_snapshot.xlsx, 2026-03-02_snapshot.xlsx.",
        ],
    ),
    (
        "Bottom-Line Ask",
        [
            "To recreate the workbook properly week on week, I need full weekly resource-level snapshots rather than only summarized billed or unbilled counts.",
            "I need current and previous week billing and project state, reason codes, billing-plan fields, L2 to L4 hierarchy, FTE or allocation at row level, and ownership and segmentation fields.",
        ],
    ),
]


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


body = [p(TITLE, "Title")]
for heading, bullets in SECTIONS:
    body.append(p(heading, "Heading1"))
    for item in bullets:
        body.append(p(item))

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
    + "".join(body)
    + (
        "<w:sectPr>"
        "<w:pgSz w:w=\"12240\" w:h=\"15840\"/>"
        "<w:pgMar w:top=\"1440\" w:right=\"1440\" w:bottom=\"1440\" w:left=\"1440\" w:header=\"708\" w:footer=\"708\" w:gutter=\"0\"/>"
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
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/>
    <w:basedOn w:val="Normal"/>
    <w:qFormat/>
    <w:rPr><w:b/><w:sz w:val="32"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:basedOn w:val="Normal"/>
    <w:qFormat/>
    <w:rPr><w:b/><w:sz w:val="24"/></w:rPr>
  </w:style>
</w:styles>
"""

core_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
 xmlns:dc="http://purl.org/dc/elements/1.1/"
 xmlns:dcterms="http://purl.org/dc/terms/"
 xmlns:dcmitype="http://purl.org/dc/dcmitype/"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>CUNB Weekly Data Requirements and Asks</dc:title>
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

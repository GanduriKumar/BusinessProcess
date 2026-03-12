from pathlib import Path
from xml.sax.saxutils import escape
import zipfile


OUTPUT = Path(r"C:\users\kumar.gn\HClProjects\BusinessProcess\CUNB-2 Mar 2026 Analysis.docx")

TITLE = "Analysis of CUNB-2 Mar'26 V.1.xlsx"

PARAGRAPHS = [
    "The workbook CUNB-2 Mar'26 V.1.xlsx is a March 2026 CUNB tracking model centered on the snapshot for March 2, 2026. It combines a large raw extract, pivot-style summary sheets, weekly movement views, contributor commentary, and dashboard charts. Structurally it has 31 sheets total: 19 visible, 12 hidden, plus 24 embedded charts, 2 drawings, and 2 external links.",
    "At a high level, the file tracks unbilled headcount and FTE across L2 and L3 structures, customers, billing plans, no-plan buckets, movements week over week, and exclusions such as freshers, support, delivery reasons, and investments.",
    "The workbook is organized into several layers. Raw and base data sits in Export, CUNB, weekly Base, and Approved investment. Summary and management views sit in L2 Wise, Overall CUNB, No plan, Billing Plan, Investment Summary, and E and Y Code. Operational movement views include Weekly Status, Week on Week Summary, JFM Weekly Walk, Billed to Unbilled, and Insight Walk. Specialized subsets include top contributors, Freshers Summary, and Divas summary.",
    "The L2 trend uses weekly snapshots from June 30, 2025 through March 2, 2026. The L2 unbilled trend rises from 537 on June 30, 2025 to a peak of 912.31 on October 13, 2025, spikes again to 905 on January 5, 2026, then falls before rebounding sharply to 738 on March 2, 2026. The immediate week-over-week move into March 2, 2026 is a jump of 170 FTE from February 23, 2026.",
    "From the L2 Wise summary, the March 2, 2026 total CUNB is 738.14 FTE. That total is decomposed into Billed to Unbilled at 44, Unbilled_No changes at 472.60, VDU tech or movement bucket at 167, and Partial billed to unbilled - CSG at 54.54. A related movement block shows Got billed at 43, Moved out at 53, Unbilled VDU to CU at 1, Unbilled_No changes at 471.37, and a remaining carry-forward style total at 568.37.",
    "Overall CUNB contains two major reason-based blocks. The full CUNB total is 738.14. The largest reason buckets in that full pool are Extra Effort at 208.72, ICB - Project Specific Induction Training at 151.15, Freshers at 80, Delivery Manager at 72.43, IFD Resources at 65.01, Long Leave at 59, and Support Resource at 29.3. This shows the population is not driven by only one commercial issue; a large share is operational, transitional, or non-actionable in nature.",
    "The second Overall CUNB block represents a tighter unbilled-no-change style subset totaling 568.37. Its biggest drivers are Extra Effort at 150.96, ICB - Project Specific Induction Training at 102.55, Freshers at 86, Delivery Manager at 60.56, Long Leave at 57, IFD Resources at 40, and Support Resource at 34.3.",
    "The No plan sheet is filtered to LATERAL and Billing Status2 equal to No Billing planned. The grand total is 141.58 FTE. The largest no-plan reasons are Non billable 1 hrs-CSG at 28.77, Bench Movement at 25, Support/DM/PM at 24.01, Approved Investment at 19, Partial assigned at 12.8, Wrong assignation at 6, Bench Constraint at 5, Moving to CU at 4, ML Case at 4, and ML Returnee at 4.",
    "By L3, the no-plan total is concentrated in META&CSG at 67.08 and SERVICE VERTICALS at 39.5, followed by ALPHABET at 15, ECP at 10.5, MS COMPUTE TECHNOLOGY at 7, MS CORE ENG at 2, and STARSCHEMA at 0.5. This concentration suggests that much of the no-plan burden is not simple demand shortfall but a mix of assignment hygiene, support roles, investments, movement, and classification issues.",
    "The Billing Plan sheet shows a planned billing total of 224.88 FTE. The monthly distribution is heavily concentrated in March 2026 at 165.54, with 16.34 in February 2026, 30 in April 2026, 5 in May 2026, 5 in July 2026, and 1 in August 2026. The plan therefore depends strongly on March conversion.",
    "The largest customers in the Billing Plan are MICROSOFT CORPORATION at 50, Google LLC at 37, Pearson Technology at 17, Sirius XM Radio Inc. at 16, Western Union Inc at 14, SAMSUNG DATA SYSTEMS INDIA PVT LTD at 12, and Mastercard Technologies LLC at 11.",
    "Using the visible headline summaries, total CUNB is 738.14, Billing Plan is 224.88, and No Plan is 141.58. The remainder sits in movement, exclusion, and operational action buckets rather than in a simple planned-versus-not-planned split. That is consistent with the workbook design, which tracks billing execution together with movement and non-actionable classifications.",
    "The top contributors sheet identifies the largest customer concentrations. HCL Technologies Ltd. contributes 66.82 FTE or 17.65 percent, MICROSOFT CORPORATION 59 or 15.59 percent, Google LLC 52 or 13.74 percent, Pearson Technology 24 or 6.34 percent, Western Union Inc 19 or 5.02 percent, Sirius XM Radio Inc. 16 or 4.23 percent, Meta Platforms, Inc. 14 or 3.70 percent, The Gap Inc. 13.05, Mastercard Technologies LLC 13, SAMSUNG DATA SYSTEMS INDIA PVT LTD 12, and PayPal Inc. 6.51. These top contributors total 295.38 FTE and account for roughly 78 percent of the share represented in that sheet, which means the issue is concentrated rather than broadly dispersed.",
    "Embedded remarks in top contributors indicate recurring themes: customer approval delays, SOW awaited, onboarding still in progress, approved investments, buffer resources, bench movement, and support or PMO roles sitting in unbilled pools. This supports the view that execution and process timing are as material as pure demand creation.",
    "Weekly Status acts as a management control sheet. It tracks weekly L3 and L4 customer rows with fields for Total CUNB, Incoming CUNB, expected joining, rampdown and issue buckets, outgoing CUNB, overall current week, excluded CUNB, freshers, and delivery-driven exclusions. Aggregated current-week totals move as follows: Week 1 at 620.11, Week 2 at 709.50, Week 3 at 700.96, Week 4 at 646.65, Week 5 at 632.80, Week 6 at 678.30, Week 7 at 561.80, Week 8 at 555.60, Week 9 at 691.11, Week 10 at 689.56, Week 11 at 659.96, Week 12 at 582.86, Week 13 at 398.66, Week 14 at 431.66, Week 15 at 401.71, Week 16 at 466.95, and Week 17 at 672.15.",
    "For the latest week, Week 17 aligned to March 2, 2026, Total CUNB at 90 percent coverage is 655.65, Incoming CUNB is 58, Billing by next week is 41.5, Outgoing CUNB is 41.5, Overall current week is 672.15, and Overall Exclude CUNB is 658.16. The sheet therefore shows a sharp rebound in the active management total.",
    "Examples from Week 17 show amber-status cases such as The Gap at 22.05, Time Warner at 13, National Westminster Bank at 12.7, Samsung at 12, Ulta at 9, and Apple at 7.6. Green cases include NortonLifeLock at 4.5 and J.Crew reaching zero after planned outgoing actions. This suggests the sheet is intended for weekly execution review and prioritization.",
    "Freshers Summary and Divas summary show that a meaningful portion of the population sits in fresher or special-utilization pools. In Freshers Summary, SERVICE VERTICALS totals 74, MS CORE ENG 67, ALPHABET 59, META&CSG 56, ECP 37.3, and MS COMPUTE TECHN 10. In Divas summary, the grand total is 107, with MS CORE ENG showing the highest utilization at 70 percent and SERVICE VERTICALS and ECP nearer 29 percent.",
    "Investment Summary totals 26 FTE. Google LLC accounts for 14, Meta Platforms, Inc. 7, MICROSOFT CORPORATION 4, and Ulta Inc 1. Approver labels include L3 head, L4 head, L2 Head, and L2H to approve. One row appears to have a reversed start and end date, which suggests a source data quality issue.",
    "The E and Y Code sheet shows that C code has a much stronger planned-billing profile than E code. C code shows 129.5 in Billing Planned and 52 in No Billing planned for a total of 181.5. E code shows 55.74 in Billing Planned and 95.98 in No Billing planned for a total of 151.72. The sheet also tracks Y code separately in the same pattern.",
    "The Dashboard sheet itself is chart-driven rather than table-driven. Embedded chart titles include L2-Tech CUNB trend, Actionable vs Non Actionable, Freshers versus lateral, Onshore/Offshore/Nearshore splits, and L3-specific utilization or contribution views for Alphabet, ECP, Meta, MS Compute, MS Core, Service Verticals, and Starschema. The workbook is therefore intended as both an operating model and a leadership presentation pack.",
    "There are a few structural and data-quality caveats. Overall CUNB contains some formula error cells such as #VALUE!. The workbook contains hidden duplicate or helper sheets like Overall CUNB (2), No plan (2), and Billing Plan (2). It also contains external links, which means some outputs may depend on upstream sources not fully embedded in the file. Date serials are used heavily, increasing interpretation risk if date formatting changes.",
    "The bottom-line reading is that the workbook is a management control file for March 2, 2026 CUNB, not just a raw extract. The main message is that CUNB is materially elevated at 738.14 FTE, the biggest immediate pool is Unbilled_No changes at 472.60, only 224.88 FTE sits in explicit billing plan, and 141.58 FTE sits in no-plan lateral buckets. The issue is concentrated in a relatively small set of customers and L3s, especially Microsoft, Google, HCL Technologies Ltd., Pearson, Western Union, Meta, Service Verticals, and Meta&CSG.",
    "The operational conclusion is that this is not only a sales conversion problem. It is a blended issue of billing execution, assignment cleanup, fresher and bench handling, movement timing, customer approval and SOW lag, and role hygiene. Any reduction plan that treats the entire CUNB pool as commercially actionable would overstate what can realistically be converted in the near term.",
]


def make_paragraph(text: str, style: str | None = None) -> str:
    style_xml = ""
    if style:
        style_xml = f"<w:pPr><w:pStyle w:val=\"{style}\"/></w:pPr>"
    return (
        "<w:p>"
        f"{style_xml}"
        "<w:r><w:t xml:space=\"preserve\">"
        f"{escape(text)}"
        "</w:t></w:r>"
        "</w:p>"
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
    f"{make_paragraph(TITLE, 'Title')}"
    + "".join(make_paragraph(p) for p in PARAGRAPHS)
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
    <w:rPr>
      <w:b/>
      <w:sz w:val="32"/>
    </w:rPr>
  </w:style>
</w:styles>
"""

core_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
 xmlns:dc="http://purl.org/dc/elements/1.1/"
 xmlns:dcterms="http://purl.org/dc/terms/"
 xmlns:dcmitype="http://purl.org/dc/dcmitype/"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>Analysis of CUNB-2 Mar'26 V.1.xlsx</dc:title>
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

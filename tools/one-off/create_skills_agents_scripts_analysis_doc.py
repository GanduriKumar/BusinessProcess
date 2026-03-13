from pathlib import Path
from xml.sax.saxutils import escape
import zipfile


OUTPUT = Path(
    r"C:\Users\kumar.gn\HCLProjects\BusinessProcess\docs\output\Skills and Agents Script Recommendations.docx"
)

TITLE = "Skills and Agents Script Recommendations"
SUBTITLE = "Assessment of the current skills and agents structure, with recommendations on where automation scripts would add the most value."


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


body = [p(TITLE, "Title"), p(SUBTITLE, "Subtitle")]

body.append(p("1. Executive Summary", "Heading1"))
body.append(
    p(
        "The current repo structure for skills and agents is directionally sound. The skills define task-level workflows and the agents define repo-level specialist personas. The main gap is not structure; it is the absence of a small number of deterministic scripts for repeated document extraction, template application, and spreadsheet summarization tasks."
    )
)
body.append(
    p(
        "Scripts are most justified where the repo repeatedly handles structured inputs such as RFP questionnaires, PDF or PPTX-based templates, and spreadsheet-based financial or operational reports. In those cases, automation would reduce manual effort and improve consistency."
    )
)

body.append(p("2. What is working well", "Heading1"))
body.append(p("- The repo cleanly separates skills from agents."))
body.append(p("- The skills have clear trigger conditions and focused references."))
body.append(p("- The agents have practical scopes, workflows, and starter templates."))
body.append(p("- The current setup is maintainable and understandable without extra tooling."))

body.append(p("3. Where scripts are recommended", "Heading1"))
body.append(
    p(
        "3.1 RFP response"
    )
)
body.append(
    p(
        "The RFP workflow is the strongest candidate for scripts because it repeatedly depends on extracting structured requirements, building response matrices, and applying a response template."
    )
)
body.append(p("Recommended scripts:"))
body.append(p("- skills/rfp-response/scripts/extract_rfp_questions.py"))
body.append(p("- skills/rfp-response/scripts/build_compliance_matrix.py"))
body.append(p("- skills/rfp-response/scripts/apply_response_template.py"))

body.append(
    p(
        "3.2 Internal leadership storytelling"
    )
)
body.append(
    p(
        "This skill now depends on a PDF template as a default framing asset. A script would make that template easier to reuse consistently by extracting the content into a more usable intermediate form."
    )
)
body.append(p("Recommended script:"))
body.append(p("- skills/internal-leadership-storytelling/scripts/extract_story_template.py"))

body.append(
    p(
        "3.3 Business financial analysis"
    )
)
body.append(
    p(
        "Financial analysis would benefit from a small set of scripts that normalize spreadsheet inputs and generate a repeatable variance or driver summary."
    )
)
body.append(p("Recommended scripts:"))
body.append(p("- skills/business-financial-analysis/scripts/load_financial_model.py"))
body.append(p("- skills/business-financial-analysis/scripts/variance_summary.py"))

body.append(
    p(
        "3.4 Operational data analysis"
    )
)
body.append(
    p(
        "Operational analysis would benefit from scripts that standardize columns, normalize category values, and generate a KPI snapshot from common reports."
    )
)
body.append(p("Recommended scripts:"))
body.append(p("- skills/operational-data-analysis/scripts/normalize_ops_report.py"))
body.append(p("- skills/operational-data-analysis/scripts/kpi_snapshot.py"))

body.append(
    p(
        "3.5 Slide deck creation"
    )
)
body.append(
    p(
        "The deck skill already encourages programmatic generation, but it does not yet package reusable helpers inside the skill itself."
    )
)
body.append(p("Recommended scripts:"))
body.append(p("- skills/slide-deck-creation/scripts/init_business_deck.py"))
body.append(p("- skills/slide-deck-creation/scripts/extract_slide_text.py"))

body.append(p("4. Priority order", "Heading1"))
body.append(
    p(
        "Recommended implementation order:"
    )
)
body.append(p("1. RFP response"))
body.append(p("2. Internal leadership storytelling"))
body.append(p("3. Business financial analysis"))
body.append(p("4. Operational data analysis"))
body.append(p("5. Slide deck creation"))

body.append(p("5. First wave recommendation", "Heading1"))
body.append(
    p(
        "If only a small first wave of scripts is created, the highest-value set is:"
    )
)
body.append(p("- skills/rfp-response/scripts/extract_rfp_questions.py"))
body.append(p("- skills/rfp-response/scripts/build_compliance_matrix.py"))
body.append(p("- skills/internal-leadership-storytelling/scripts/extract_story_template.py"))
body.append(p("- skills/business-financial-analysis/scripts/variance_summary.py"))
body.append(p("- skills/operational-data-analysis/scripts/kpi_snapshot.py"))

body.append(p("6. Bottom Line", "Heading1"))
body.append(
    p(
        "The repo does need scripts, but only in the high-repeat, structure-heavy areas. The best approach is to add a small number of skill-local scripts that automate extraction, normalization, and first-pass summaries, while leaving business judgment and storytelling in the skills and agents themselves."
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
    + "".join(body)
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
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"/>
"""

styles_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:qFormat/>
    <w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/>
    <w:basedOn w:val="Normal"/>
    <w:qFormat/>
    <w:pPr><w:spacing w:after="160"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="34"/><w:szCs w:val="34"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Subtitle">
    <w:name w:val="Subtitle"/>
    <w:basedOn w:val="Normal"/>
    <w:qFormat/>
    <w:pPr><w:spacing w:after="220"/></w:pPr>
    <w:rPr><w:i/><w:color w:val="5A5A5A"/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:basedOn w:val="Normal"/>
    <w:next w:val="Normal"/>
    <w:qFormat/>
    <w:pPr><w:spacing w:before="220" w:after="120"/></w:pPr>
    <w:rPr><w:b/><w:color w:val="1F4E79"/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr>
  </w:style>
</w:styles>
"""

core_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
 xmlns:dc="http://purl.org/dc/elements/1.1/"
 xmlns:dcterms="http://purl.org/dc/terms/"
 xmlns:dcmitype="http://purl.org/dc/dcmitype/"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>Skills and Agents Script Recommendations</dc:title>
  <dc:creator>OpenAI Codex</dc:creator>
  <cp:lastModifiedBy>OpenAI Codex</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">2026-03-13T00:00:00Z</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">2026-03-13T00:00:00Z</dcterms:modified>
</cp:coreProperties>
"""

app_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
 xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Microsoft Office Word</Application>
</Properties>
"""


OUTPUT.parent.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(OUTPUT, "w", compression=zipfile.ZIP_DEFLATED) as docx:
    docx.writestr("[Content_Types].xml", content_types_xml)
    docx.writestr("_rels/.rels", rels_xml)
    docx.writestr("word/document.xml", document_xml)
    docx.writestr("word/_rels/document.xml.rels", document_rels_xml)
    docx.writestr("word/styles.xml", styles_xml)
    docx.writestr("docProps/core.xml", core_xml)
    docx.writestr("docProps/app.xml", app_xml)

print(f"Created {OUTPUT}")

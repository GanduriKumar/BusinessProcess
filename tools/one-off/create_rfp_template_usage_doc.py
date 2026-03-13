from pathlib import Path
from xml.sax.saxutils import escape
import zipfile


OUTPUT = Path(
    r"C:\Users\kumar.gn\HCLProjects\BusinessProcess\docs\output\RFP Template Placement and Invocation Guide.docx"
)

TITLE = "RFP Template Placement and Invocation Guide"
SUBTITLE = "Guidance for where to store the RFP response template, how to reference it, and how to invoke response generation."


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

body.append(p("1. Where to add the RFP template and how to reference it", "Heading1"))
body.append(
    p(
        "The right location depends on whether the template is skill-specific or agent-specific."
    )
)
body.append(
    p(
        "Use the skill directory when the template is part of the reusable RFP capability itself and should apply regardless of which repo-level agent is driving the work."
    )
)
body.append(p("- Recommended skill location: C:\\Users\\kumar.gn\\HCLProjects\\BusinessProcess\\skills\\rfp-response\\templates\\"))
body.append(
    p(
        "Example skill-specific template path:"
    )
)
body.append(
    p(
        "- C:\\Users\\kumar.gn\\HCLProjects\\BusinessProcess\\skills\\rfp-response\\templates\\customer-rfp-response-template.docx"
    )
)
body.append(
    p(
        "Use the agent directory only when the template is specific to how one repo-level agent packages or presents the response, and not to the RFP skill overall."
    )
)
body.append(p("- Agent-specific location: C:\\Users\\kumar.gn\\HCLProjects\\BusinessProcess\\agents\\proposal-manager\\templates\\"))
body.append(
    p(
        "Example agent-specific template path:"
    )
)
body.append(
    p(
        "- C:\\Users\\kumar.gn\\HCLProjects\\BusinessProcess\\agents\\proposal-manager\\templates\\proposal-manager-packaging-template.md"
    )
)
body.append(
    p(
        "Recommended location in most cases: store the customer or response template in the skill directory, not the agent directory."
    )
)
body.append(
    p(
        "Reason: an RFP response template is usually a task-level asset. It belongs to the reusable RFP capability and should be available whether the response is driven by proposal-manager or by any future agent that uses the same skill."
    )
)
body.append(
    p(
        "Recommended setup:"
    )
)
body.append(
    p(
        "- Store the primary customer response template under skills/rfp-response/templates/."
    )
)
body.append(
    p(
        "- Reference that template from skills/rfp-response/SKILL.md as the default template for this skill."
    )
)
body.append(
    p(
        "- If proposal-manager should use it by default, add a pointer in agents/proposal-manager/AGENT.md or agents/proposal-manager/workflows/rfp-delivery.md to the skill-level template path."
    )
)
body.append(
    p(
        "- Use the agent templates folder only for agent-specific wrappers, review formats, or packaging structures."
    )
)
body.append(
    p(
        "A practical instruction line in the skill or agent can look like this:"
    )
)
body.append(
    p(
        "Use the response template at skills/rfp-response/templates/customer-rfp-response-template.docx when drafting proposal responses unless the user provides a different customer-issued format."
    )
)
body.append(
    p(
        "If the customer gives a DOCX or XLSX response form, store that file under the skill templates folder and reference the exact file path in the request so the skill and agent both use the same source of truth."
    )
)

body.append(p("2. How to invoke RFP response generation", "Heading1"))
body.append(
    p(
        "To invoke RFP response generation well, provide four things in the request:"
    )
)
body.append(p("- The source RFP or questionnaire files"))
body.append(p("- The response template path"))
body.append(p("- The expected output format, such as DOCX, XLSX, or draft Markdown"))
body.append(p("- Any audience or tone constraint, such as executive, evaluator-friendly, concise, or detailed"))
body.append(
    p(
        "A strong invocation pattern is:"
    )
)
body.append(
    p(
        "Use proposal-manager and the rfp-response skill to draft the response. Source files are <path>. Use the template at <path>. Produce a compliant first draft in <format> and flag any gaps or unsupported claims."
    )
)
body.append(
    p(
        "Example:"
    )
)
body.append(
    p(
        "Use proposal-manager to create an RFP response from C:\\Users\\kumar.gn\\HCLProjects\\BusinessProcess\\docs\\input\\customer-rfp.docx. Use the template at C:\\Users\\kumar.gn\\HCLProjects\\BusinessProcess\\skills\\rfp-response\\templates\\customer-rfp-response-template.docx. Produce a first draft in DOCX and include a compliance-gap list."
    )
)
body.append(
    p(
        "If you want a review pass instead of full generation, invoke it like this:"
    )
)
body.append(
    p(
        "Use proposal-manager to review the attached RFP response against the template at <path>. Identify missing requirement coverage, unsupported claims, and sections that need tightening."
    )
)
body.append(
    p(
        "The most important practical rule is to mention the exact template path in the prompt. That removes ambiguity and makes it clear which repo template the agent should follow."
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
  <dc:title>RFP Template Placement and Invocation Guide</dc:title>
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

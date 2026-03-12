from pathlib import Path
from xml.sax.saxutils import escape
import zipfile


OUTPUT = Path(
    r"C:\Users\kumar.gn\HCLProjects\BusinessProcess\docs\Google Search GEO Research.docx"
)
TITLE = "How GEO Helps, If At All, In Google Search"
SUBTITLE = (
    "Research note on whether generative engine optimization (GEO) materially improves "
    "performance in Google Search, AI Overviews, and AI Mode."
)


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
    bold = "<w:b/>" if header else ""
    return (
        "<w:tc>"
        f"<w:tcPr><w:tcW w:w=\"{width}\" w:type=\"dxa\"/>{shade}</w:tcPr>"
        "<w:p><w:r><w:rPr>"
        f"{bold}<w:sz w:val=\"20\"/>"
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


body = [p(TITLE, "Title"), p(SUBTITLE, "Subtitle")]

body.append(p("1. Executive Summary", "Heading1"))
body.append(
    p(
        "GEO, or generative engine optimization, is not a formal Google Search program or ranking framework. Google does not currently publish a separate GEO rulebook for AI Overviews or AI Mode."
    )
)
body.append(
    p(
        "The practical answer is that GEO helps only to the extent that it overlaps with strong SEO, clear information architecture, structured data where appropriate, and content that is genuinely useful, crawlable, and easy for Google to interpret."
    )
)
body.append(
    p(
        "If GEO means rewriting pages to be concise, explicit, entity-rich, and factually well-structured, that can help because it improves standard search quality signals and machine readability. If GEO means trying to stuff pages with answer-like text or AI bait without adding value, Google's guidance does not support that approach."
    )
)

body.append(p("2. What Google Officially Says", "Heading1"))
body.append(
    table(
        ["Topic", "Google's position", "Implication for GEO"],
        [
            [
                "AI search performance",
                "Google says its core SEO guidance applies to AI experiences in Search.",
                "There is no separate GEO playbook replacing SEO.",
            ],
            [
                "Content quality",
                "Google tells site owners to focus on unique, valuable content made for people.",
                "Useful information helps; generic AI-flavored rewrites do not create a new advantage by themselves.",
            ],
            [
                "Technical accessibility",
                "Google says it must be able to access content and render pages properly.",
                "Machine readability matters, but mostly through standard crawlability and page construction.",
            ],
            [
                "Preview controls",
                "Google says publishers can manage visibility with preview controls such as nosnippet and max-snippet settings.",
                "This affects whether content can be used in AI surfaces, but it is a visibility control, not a GEO boost.",
            ],
            [
                "Structured data",
                "Google says structured data should match visible page content.",
                "Schema can help Google understand pages, but only when tied to real, visible information.",
            ],
        ],
        [1800, 3600, 3600],
    )
)

body.append(p("3. Where GEO Can Actually Help", "Heading1"))
for item in [
    "Clear answer structure. Pages that answer a question directly, then expand with detail, are easier for Google to parse and summarize.",
    "Entity clarity. Explicitly naming products, people, companies, dates, locations, and relationships reduces ambiguity.",
    "Information hierarchy. Strong headings, logical sections, tables, lists, and short factual blocks make extraction easier.",
    "Source-backed claims. Citing primary evidence and keeping claims specific improves trustworthiness.",
    "Consistent terminology. Using one name per concept helps both traditional ranking systems and AI summarization systems.",
    "Structured data where relevant. Product, FAQ, article, organization, review, and other supported markup can improve interpretability if it matches visible content.",
    "Freshness on time-sensitive pages. For topics where current information matters, keeping pages updated helps Google trust the page for current answers.",
    "Strong internal linking. Clear links between hub pages, definitions, products, and source pages help Google connect context.",
]:
    body.append(p(f"- {item}"))

body.append(p("4. Where GEO Probably Does Not Help Much", "Heading1"))
for item in [
    "Keyword stuffing with AI-oriented phrases such as 'best answer for AI assistants' or similar boilerplate.",
    "Publishing thin pages designed only to be quoted by chatbots without adding original value.",
    "Overusing FAQ blocks or schema solely to chase rich results when the page itself is weak.",
    "Generating large volumes of low-differentiation content with AI and expecting Google to reward scale alone.",
    "Assuming that conversational tone alone improves AI visibility.",
    "Treating GEO as a substitute for authority, reputation, original reporting, product depth, or technical SEO.",
]:
    body.append(p(f"- {item}"))

body.append(p("5. GEO Versus SEO in Google Search", "Heading1"))
body.append(
    table(
        ["Question", "Traditional SEO", "GEO in Google context"],
        [
            [
                "Is it officially defined by Google",
                "Yes, through extensive Search Central documentation.",
                "No, not as a standalone Google framework.",
            ],
            [
                "Primary goal",
                "Rank and earn clicks in Search surfaces.",
                "Make content easy for generative systems to understand and cite.",
            ],
            [
                "What actually drives results on Google",
                "Quality, relevance, technical access, links, experience, and intent match.",
                "Mostly the same things, plus good summarizability and explicit structure.",
            ],
            [
                "Should a business create a separate team/process",
                "Usually part of existing organic search and content work.",
                "Only if it means tightening content structure and evidence quality, not inventing a disconnected discipline.",
            ],
        ],
        [2500, 3100, 3500],
    )
)

body.append(p("6. How GEO Relates to AI Overviews and AI Mode", "Heading1"))
body.append(
    p(
        "For Google AI Overviews and AI Mode, the strongest interpretation from official guidance is that Google continues to use its existing Search understanding systems, ranking systems, and content access rules, then applies generative presentation on top of them."
    )
)
body.append(
    p(
        "That means GEO is useful only when it makes a page more eligible for Google's existing systems to trust, understand, and summarize. It is not a paid shortcut, and it is not a separate optimization layer that overrides SEO fundamentals."
    )
)

body.append(p("7. Practical Recommendations", "Heading1"))
body.append(
    table(
        ["Action", "Why it is worth doing"],
        [
            [
                "Rewrite key pages around explicit questions and tasks",
                "Improves direct answerability and user comprehension.",
            ],
            [
                "Add concise definitions, comparison tables, and step-by-step sections where relevant",
                "Makes pages easier to summarize and quote.",
            ],
            [
                "Strengthen factual specificity with dates, numbers, constraints, and examples",
                "Reduces vagueness and improves credibility.",
            ],
            [
                "Use schema only where Google officially supports it",
                "Avoids fake precision and keeps markup aligned with visible content.",
            ],
            [
                "Audit snippet controls and crawlability",
                "Ensures Google is allowed to use page content in AI and Search experiences.",
            ],
            [
                "Remove thin, duplicative, or generic AI-generated pages",
                "Prevents dilution of site quality and index value.",
            ],
            [
                "Track performance in Search Console at the page and query level",
                "Lets you see whether clearer formatting improves impressions, clicks, and engagement.",
            ],
        ],
        [3300, 5900],
    )
)

body.append(p("8. Bottom Line", "Heading1"))
body.append(
    p(
        "GEO can help in Google Search, but only modestly and mostly through better execution of existing SEO principles. Google's public guidance does not indicate that GEO is a separate ranking system or a special optimization channel for AI Mode."
    )
)
body.append(
    p(
        "The useful part of GEO is cleaner structure, clearer facts, better entity framing, stronger evidence, and supported structured data. The non-useful part is treating GEO as a shortcut or as a replacement for genuine content quality, technical accessibility, and authority."
    )
)

body.append(p("9. Sources", "Heading1"))
for source in [
    "Google Search Central Blog, 'Top ways to ensure your content performs well in Google's AI experiences on Search' (May 21, 2025): https://developers.google.com/search/blog/2025/05/succeeding-in-ai-search",
    "Google Search blog, 'Expanding AI Overviews and introducing AI Mode' (March 5, 2025): https://blog.google/products-and-platforms/products/search/ai-mode-search/",
    "Google Search Central, 'Google Search's guidance about AI-generated content' (accessed March 12, 2026): https://developers.google.com/search/docs/fundamentals/using-gen-ai-content",
    "Google Search Central, 'Control what you share with Google' preview controls documentation (accessed March 12, 2026): https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag",
    "Google Search Central, structured data guidance (accessed March 12, 2026): https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data",
]:
    body.append(p(source))


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
    <w:rPr>
      <w:sz w:val="22"/>
      <w:szCs w:val="22"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/>
    <w:basedOn w:val="Normal"/>
    <w:qFormat/>
    <w:pPr><w:spacing w:after="160"/></w:pPr>
    <w:rPr>
      <w:b/>
      <w:sz w:val="34"/>
      <w:szCs w:val="34"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Subtitle">
    <w:name w:val="Subtitle"/>
    <w:basedOn w:val="Normal"/>
    <w:qFormat/>
    <w:pPr><w:spacing w:after="220"/></w:pPr>
    <w:rPr>
      <w:i/>
      <w:color w:val="5A5A5A"/>
      <w:sz w:val="22"/>
      <w:szCs w:val="22"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:basedOn w:val="Normal"/>
    <w:next w:val="Normal"/>
    <w:qFormat/>
    <w:pPr><w:spacing w:before="220" w:after="120"/></w:pPr>
    <w:rPr>
      <w:b/>
      <w:color w:val="1F4E79"/>
      <w:sz w:val="26"/>
      <w:szCs w:val="26"/>
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
  <dc:title>How GEO Helps, If At All, In Google Search</dc:title>
  <dc:creator>OpenAI Codex</dc:creator>
  <cp:lastModifiedBy>OpenAI Codex</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">2026-03-12T00:00:00Z</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">2026-03-12T00:00:00Z</dcterms:modified>
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

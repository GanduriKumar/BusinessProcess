# AI Search Discovery Research Paper

## Goal

Produce a source-backed technical paper on how Google Search changed with AI Overviews and AI Mode and how content teams should adapt for AI-native discovery surfaces across Google and other answer engines.

## Steps

1. Refresh the configured primary-source snapshot with:
   - `python skills/ai-search-discovery-research/scripts/build_source_snapshot.py`
2. Review the latest source snapshot under:
   - `docs/output/websearch/search-discovery/`
3. Generate the technical paper draft with:
   - `python skills/ai-search-discovery-research/scripts/scaffold_technical_paper.py`
4. Review the generated paper and refine any sections that need more evidence depth or tighter platform-specific recommendations.
5. Validate that the paper distinguishes:
   - documented platform behavior
   - source-backed inference
   - unsupported folklore that should be excluded

## Validation

- Google claims are grounded in Search Central docs or official Google product posts.
- Other engine sections use official help-center, publisher, or webmaster sources where available.
- The paper includes actionable guidance for blogs, articles, docs, Medium, and LinkedIn.
- The final action plan is concrete enough for editorial, SEO, and content-ops teams to execute.

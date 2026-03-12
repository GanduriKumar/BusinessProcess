---
name: business-financial-analysis
description: Use this skill for revenue, cost, margin, pricing, P&L, business case, investment, forecast, variance, and financial performance analysis from spreadsheets, reports, or business data. Trigger when the task requires calculations, unit economics, or financially grounded recommendations.
---

# Business Financial Analysis

Use this skill for business and finance analysis. Pair it with [business-work-common](../business-work-common/SKILL.md) for shared standards.

## Primary Goal

Turn raw financial data into a clear business answer with traceable assumptions, calculations, and implications.

## Typical Inputs

- Revenue and cost spreadsheets
- Pricing models
- Budget vs actual data
- Forecast files
- Account- or portfolio-level business metrics
- Business case inputs

## Workflow

### 1. Understand the financial question

- Identify the metric the user actually cares about: revenue, gross margin, operating margin, contribution, CAC, payback, ROI, cash impact, or variance.
- Identify the time horizon and reporting grain.
- Identify whether the user wants diagnosis, forecast, or recommendation.

### 2. Normalize the data

- Standardize periods, currencies, units, and sign conventions.
- Separate one-time items from run-rate items.
- Identify missing values, duplicated rows, and inconsistent categories.

### 3. Analyze with explicit logic

- Show how each conclusion is derived.
- Distinguish actuals from forecasts.
- Label assumptions, scenario drivers, and sensitivity points.
- Reconcile totals to source data before summarizing.

### 4. Convert analysis into business language

- Explain what moved, why it moved, and what matters next.
- Separate controllable drivers from external factors.
- Recommend actions only when the driver logic is clear.

## Default Output Pattern

1. Executive answer
2. Key metrics and period
3. Driver analysis
4. Risks and assumptions
5. Recommendation or next step

## Minimum Financial Hygiene

- Every percentage should have a base.
- Every trend should have a period.
- Every forecast should state the assumption.
- Every benefit claim should tie back to arithmetic.

## References

- Shared standard: [business-work-common](../business-work-common/SKILL.md)
- Checklist: [references/financial-analysis-checklist.md](references/financial-analysis-checklist.md)

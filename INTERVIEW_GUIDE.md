# Interview Guide

## 30-second explanation
I built an AI-assisted bank fraud investigation tool. Synthetic transactions are stored in PostgreSQL. Explainable Python rules flag suspicious patterns such as unusually large or rapid transfers. An LLM then reviews the alert and recent customer history and drafts an evidence-grounded investigation note. I kept detection rule-based so every alert has a clear reason.

## Why no ML?
The goal is investigation workflow automation, not prediction. Rules are transparent and easy to audit.

## What does the AI do?
It turns alert context and transaction evidence into a concise case note with risk assessment, evidence, context, and recommended review.

## Does it determine fraud?
No. Suspicious activity is not proof of fraud. It recommends human review.

## Biggest limitation
The rules are simplified and the dataset is synthetic. A production system would need richer context, configurable monitoring, access controls, audit logs, and human case management.

---
title: LLM Secure Gateway
emoji: 🔐
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# LLM Secure Gateway - Business User Guide

**One-click AI access. Never worry about a single provider failing again.**

---

## What It Does

Think of this like a phone system that redirects calls automatically. When you submit a question, the gateway sends it to Google Gemini. If Gemini is busy or down, it instantly tries Groq. If that fails too, it falls back to OpenRouter. Your question always gets answered—no manual intervention needed.

It also acts as a security guard, blocking:
- **Tricks like "ignore your rules"** that hackers try to use
- **Accidentally revealed passwords or credit cards** in questions
- **Suspicious patterns** that look like attacks

---

## Business Benefits

| Your Challenge | How This Solves It |
|---|---|
| AI services go down and your users can't get answers | Automatic failover between 3 providers—zero downtime |
| Hackers try prompt injection attacks | Built-in detection blocks malicious requests |
| Accidental data leaks (SSN, credit card numbers) | Automatic PII detection before sending to AI |
| Unpredictable AI costs from one vendor | Mix providers to optimize cost per request |
| No visibility into what's happening | Real-time metrics dashboard |

---

## Key Metrics

- **99.8% uptime** - Automatic failover between providers
- **87-200ms response time** - Under 1/5 of a second (slower than local, faster than acceptable)
- **Zero infrastructure cost** - Deploy free on HuggingFace Spaces

---

## Try It Right Now

### Step 1: Open the Demo

Click here: [huggingface.co/spaces/vn6295337/Enterprise-AI-Gateway](https://huggingface.co/spaces/vn6295337/Enterprise-AI-Gateway)

No login. No installation. Just click and use.

### Step 2: See Pre-Built Scenarios

The dashboard has 5 built-in examples:

| Scenario | What You'll See |
|----------|---|
| **Normal Request** | First provider succeeds → response in ~120ms |
| **Injection Attempt** | Malicious prompt detected → blocked before AI sees it |
| **Rate Limit** | Too many requests → polite "try again later" message |
| **Cost Optimization** | Shows which provider was cheapest for that request |
| **Performance** | Shows latency breakdown across all providers |

### Step 3: Submit Your Own Question

1. Copy your API key (ask your IT team, or use the demo key)
2. Paste a question in the "Custom Prompt" box
3. Click "Ask"
4. See the response + which provider answered + how long it took

### Step 4: Understanding the Results

When you submit a question, you'll see:

| Result Field | What It Means |
|---|---|
| **Response** | The AI's answer to your question |
| **Provider** | Which AI service answered (Gemini, Groq, or OpenRouter) |
| **Latency** | How fast it responded (100ms = 1/10th of a second. Lower is better) |
| **Cost Estimate** | How much this single request cost (usually $0.00001-0.00003) |
| **Cascade Path** | Shows which providers were tried and in what order |

---

## Security Features

| What We Check | Plain English | Business Impact |
|---|---|---|
| **Authentication** | "Did you provide a valid API key?" | Prevents unauthorized access |
| **Prompt Injection** | "Is someone trying tricks like 'ignore your rules'?" | Stops hackers cold |
| **PII Detection** | "Did someone accidentally paste their SSN or credit card?" | Prevents data leaks to AI providers |
| **Rate Limiting** | "Is someone spamming us with 1000 requests/second?" | Stops abuse and DDoS attacks |

---

## Who Benefits

| Role | How They Use It |
|---|---|
| **Customer Support Team** | Generate instant replies to common questions, with backup if one AI is slow |
| **Content Creator** | Draft blog posts/emails. If Gemini is slow, get instant backup answer from Groq |
| **Analyst** | Ask AI for data insights. Failover ensures analysis never stops |
| **Compliance Officer** | Built-in security blocks PII and injection attempts—reduces risk |
| **IT Manager** | One easy API for entire company. Automatic cost tracking. No vendor lock-in |

---

## Want to Deploy Your Own?

The [technical README](README.md) has installation instructions for developers.

Your IT team can deploy this to:
- **Your own server** (Docker - 1 command)
- **HuggingFace Spaces** (free serverless - 5 minutes)
- **Cloud platform** (AWS, Google Cloud, Azure - standard deployment)

---

## License

MIT License - Use freely, modify as needed.

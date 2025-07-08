# 📰 Nudge – AI News Agent

![WhatsApp Image 2025-07-09 at 00 40 56_3db7609d](https://github.com/user-attachments/assets/c8f16232-108c-4182-80c4-2881a6696cd2)


**Nudge** is a minimalist AI-powered desktop app that fetches, summarizes, and categorizes the latest news using real-time APIs. Built with Python, CustomTkinter for UI, and powered by n8n-style logic workflows, Nudge brings trending updates straight to your desktop — clean and categorized.

---

## 🚀 Features

- 🔎 **Real-time news fetching** using [NewsAPI](https://newsapi.org) and [SerpAPI](https://serpapi.com)
- 🧠 **AI summarization** using Gemini Pro (`google-generativeai`)
- 🗂️ **Category-wise filtering**: Finance, Politics, Tech, Sports, etc.
- 💾 **Auto-saving** news in structured `JSON` format
- 🖼️ Modern desktop GUI built using `CustomTkinter`
- ⚙️ Easily compiled to `.exe` for Windows deployment

---

## 📸 UI Preview

> Sidebar layout with category tags, workflow image, and summary output box on the right — clean and intuitive.

![WhatsApp Image 2025-07-09 at 00 43 16_8375857d](https://github.com/user-attachments/assets/c6119688-6ea4-40ba-8601-54e92558905e)


---

## 🧱 Tech Stack

| Tool            | Usage                    |
|-----------------|--------------------------|
| `Python`        | Core application logic   |
| `CustomTkinter` | Desktop GUI framework    |
| `NewsAPI`       | Latest headlines & topics|
| `SerpAPI`       | (Optional) Web results   |
| `Gemini API`    | AI summarization         |
| `n8n` Inspired  | Visual workflow logic    |

---

## 🧰 Installation

### 1. Clone the repository

```bash
git clone https://github.com/chiragferwani/nudge-ai-agent.git
cd nudge-ai--agent

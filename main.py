import customtkinter as ctk
import requests
import json
import google.generativeai as genai
from PIL import Image
import sys
import os
from newsapi import NewsApiClient

#-----image resource path for exe -----#
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return relative_path

# ----------API KEYS CONFIGURATION ----------#
SERP_API_KEY = "YOUR SERP API KEY"
GEMINI_API_KEY = "YOUR GEMINI API KEY"
NEWSAPI_KEY = "YOUR NEWS API KEY"
NEWS_QUERY = "latest finance news"
NUM_ARTICLES = 10

# ---------- SETUP CUSTOMTKINTER ----------#
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


# ---------- FETCH NEWS FROM SERP API ----------#
# def fetch_latest_news(query, num_articles):
#     url = f"https://serpapi.com/search.json?q={query}&tbm=nws&api_key={SERP_API_KEY}"
#     response = requests.get(url)
#
#     if response.status_code != 200:
#         raise Exception(f"SERP API Error: {response.status_code} - {response.text}")
#
#     results = response.json().get("news_results", [])
#     news_data = []
#
#     for article in results[:num_articles]:
#         title = article.get("title", "")
#         snippet = article.get("snippet", "")
#         source = article.get("source", "")
#         link = article.get("link", "")
#
#         news_data.append({
#             "title": title,
#             "description": snippet,
#             "source": source,
#             "link": link
#         })
#
#     # Save to JSON
#     with open("news_data.json", "w", encoding="utf-8") as f:
#         json.dump(news_data, f, indent=4, ensure_ascii=False)
#
#     return news_data
def fetch_latest_news(query, num_articles):
    url = f"https://serpapi.com/search.json?q={query}&tbm=nws&api_key={SERP_API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"SERP API Error: {response.status_code} - {response.text}")

    results = response.json().get("news_results", [])
    news_data = []

    for article in results[:num_articles]:
        title = article.get("title", "")
        snippet = article.get("snippet", "")
        source = article.get("source", "")
        link = article.get("link", "")

        news_data.append({
            "title": title,
            "description": snippet,
            "source": source,
            "link": link
        })

    # Save to JSON
    with open("news_data.json", "w", encoding="utf-8") as f:
        json.dump(news_data, f, indent=4, ensure_ascii=False)

    return news_data


# ---------- SUMMARIZE WITH GEMINI ----------
def summarize_with_gemini(news_items):
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(model_name="gemini-2.0-flash")

    combined_text = ""
    for news in news_items:
        combined_text += f"- {news['title']}: {news['description']}\n"

    prompt = f"""
You are an AI assistant. Summarize the following news articles into one short paragraph under 100 words.
Make it engaging and readable for social media.

{combined_text}
"""

    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.7,
            "max_output_tokens": 256
        }
    )

    return response.text.strip()


# ---------- MAIN APP ----------
class NudgeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        # self.iconbitmap(resource_path("nudge.ico"))

        # -------- NEWS QUERY ----------#
        self.selected_query = "latest trending news"  # default

        # ---------- Window Configuration ----------
        WIDTH, HEIGHT = 1000, 600
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.title("Nudge - AI News Agent")
        self.resizable(False, False)
        ctk.set_appearance_mode("light")
        self.configure(fg_color="white")

        # ---------- Fonts ----------
        font_regular = ("SF Pro Display", 14, "bold")
        font_title = ("Product Sans", 22, "bold")
        font_button = ("Product Sans", 14, "bold")

        # ---------- LEFT PANEL ----------
        self.left_panel = ctk.CTkFrame(self, width=440, height=HEIGHT, fg_color="white")
        self.left_panel.pack(side="left", fill="y")

        # Logo
        logo_img = ctk.CTkImage(light_image=Image.open(resource_path("logo.png")), size=(40, 40))
        self.logo = ctk.CTkLabel(self.left_panel, image=logo_img, text="", fg_color="white")
        self.logo.place(x=75, y=20)

        # Title
        self.title_label = ctk.CTkLabel(self.left_panel, text="NUDGE - AI News Agent",
                                        font=font_title, fg_color="white", text_color="black")
        self.title_label.place(x=125, y=25)

        # Workflow image
        workflow_img = ctk.CTkImage(light_image=Image.open(resource_path("workflow.png")), size=(400, 325))
        self.workflow_image = ctk.CTkLabel(self.left_panel, image=workflow_img, text="", fg_color="white")
        self.workflow_image.place(relx=0.5, rely=0.40, anchor="center")

        # Start Workflow Button
        self.start_button = ctk.CTkButton(self.left_panel, text="▶ START WORKFLOW",
                                          command=self.run_workflow,
                                          fg_color="#333333", font=font_button, text_color="white")
        self.start_button.place(relx=0.5, rely=0.7, anchor="center")

        # Tag Buttons (Just UI)
        tags = ["FINANCE", "EDUCATION", "POLITICAL", "TECH", "SPORTS", "GOVERNMENT", "BUSINESS", "HEALTH", "SCIENCE"]
        x_start = 30
        y_start = 460
        spacing = 120

        for i, tag in enumerate(tags):
            btn = ctk.CTkButton(self.left_panel, text=tag,
                                fg_color="#1e1e1e", text_color="white",
                                font=("Google Sans", 12, "bold"),
                                width=100, height=32,
                                hover_color="#444444",
                                command=lambda t=tag: self.set_news_category(t))
            btn.place(x=x_start + (i % 3) * spacing, y=y_start + (i // 3) * 40)

        # ---------- RIGHT PANEL ----------
        self.output_frame = ctk.CTkFrame(
            self,
            height=HEIGHT - 60,
            width=WIDTH - 480,
            corner_radius=12,
            border_width=1,
            border_color="#aaaaaa",
            fg_color="white")
        self.output_frame.place(x=450, y=30)
        self.output_frame.pack_propagate(False)
        self.output_text = ctk.CTkTextbox(self.output_frame, wrap="word", font=font_regular,fg_color="white", text_color="black")
        self.output_text.pack(padx=10, pady=10, fill="both", expand=True)

    # -------- function for setting news query ---------#
    def set_news_category(self, category):
        self.selected_query = category.lower()
        self.output_text.delete("1.0", ctk.END)
        self.output_text.insert(ctk.END, f"🔁 Selected category: {category}\n")

    def run_workflow(self):
        try:
            self.output_text.delete("1.0", ctk.END)
            self.output_text.insert(ctk.END, "🔍 Fetching news...\n\n")

            # 👇 Use self.selected_query instead of NEWS_QUERY
            news_items = fetch_latest_news(self.selected_query, NUM_ARTICLES)

            self.output_text.insert(ctk.END, f"✅ Top {len(news_items)} news articles fetched.\n\n")
            for i, item in enumerate(news_items):
                self.output_text.insert(ctk.END, f"{i + 1}. {item['title']}\n")
                self.output_text.insert(ctk.END, f"   {item['description']}\n\n")

            summary = summarize_with_gemini(news_items)
            self.output_text.insert(ctk.END, f"🧠 Summary: {summary}\n")

        except Exception as e:
            self.output_text.insert(ctk.END, f"❌ Error: {str(e)}")


# ---------- RUN APP ----------
if __name__ == "__main__":
    app = NudgeApp()
    app.mainloop()
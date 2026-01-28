import streamlit as st
import threading
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# ---------------- COMMON CHATBOT LOGIC ----------------
def get_bot_response(user_input):
    if not user_input:
        return "Please type a message so I can help you 😊"

    user_input = user_input.lower().strip()

    # Greeting
    if user_input.startswith(("hi", "hello", "hey")):
        return "Hello 👋 Welcome to our Online Book Store. How can I help you today?"

    # Book categories
    elif "book" in user_input or "books" in user_input or "categories" in user_input:
        return (
            "We offer Fiction, Non-Fiction, Academic, Competitive Exam, "
            "and Children's books.\n"
            "Please tell me what type of book you are looking for."
        )

    # Academic / student books
    elif "student" in user_input or "academic" in user_input:
        return (
            "We have textbooks, reference books, exam guides, "
            "and syllabus-based academic materials."
        )

    # Competitive exam books
    elif "competitive" in user_input or "exam" in user_input:
        return (
            "We provide books for UPSC, SSC, Banking, GATE, "
            "and other competitive examinations."
        )

    # Fiction books
    elif "fiction" in user_input or "novel" in user_input:
        return (
            "Our fiction collection includes novels, short stories, "
            "fantasy, mystery, and romance books."
        )

    # Price
    elif "price" in user_input or "cost" in user_input or "budget" in user_input:
        return "Book prices start from ₹199 and go up to ₹2,000 depending on the edition."

    # Delivery
    elif "delivery" in user_input:
        return "Books are delivered within 3 to 5 working days across India."

    # Availability
    elif "available" in user_input or "stock" in user_input:
        return "Please share the book title or author to check availability."

    # Return / Refund
    elif "return" in user_input or "refund" in user_input:
        return (
            "If you receive a damaged or incorrect book, you can request a replacement "
            "within 7 days of delivery."
        )

    # Payment
    elif "payment" in user_input:
        return (
            "We accept UPI, credit/debit cards, net banking, "
            "and cash on delivery for selected locations."
        )

    # Support
    elif "support" in user_input or "help" in user_input:
        return "Our customer support team is always happy to assist you."

    # Goodbye
    elif user_input.startswith(("bye", "thank")):
        return "Thank you for shopping with us 📚 Have a wonderful day!"

    # Default
    else:
        return (
            "Sorry, I didn’t understand that. "
            "You can ask about books, prices, delivery, or returns."
        )

# ---------------- TELEGRAM BOT ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 Welcome to the Online Book Store Support Bot!\n"
        "Ask me about books, prices, delivery, or returns."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    reply = get_bot_response(user_message)
    await update.message.reply_text(reply)

def run_telegram_bot():
    app = ApplicationBuilder().token("8340680482:AAEejEJqvZsB9yXKvdWmrrMFgiZKOXa4-C0").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

# ---------------- STREAMLIT UI ----------------
st.set_page_config(page_title="Book Shopping Chatbot", page_icon="📚")
st.title("📚 Online Book Shopping – Customer Support Chatbot")
st.write("This chatbot works on both **Streamlit Web App** and **Telegram**.")

# Start Telegram bot only once
if "telegram_started" not in st.session_state:
    threading.Thread(target=run_telegram_bot, daemon=True).start()
    st.session_state.telegram_started = True
    st.success("Telegram bot is running in the background 🚀")

# Chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("You:", placeholder="Type your message here...")

if st.button("Send"):
    if user_input.strip():
        bot_reply = get_bot_response(user_input)
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Bot", bot_reply))

# Display chat history
for sender, message in st.session_state.chat_history:
    st.markdown(f"**{sender}:** {message}")

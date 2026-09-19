# ============================================================
#   LEMINH TOOL MD5 - VIP 2026 - FINAL v7
#   Zalo: 0372834763
#   Mode: Webhook (chạy 24/7, không sleep)
# ============================================================
import os
import re
import html
import hashlib
import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# ============================================================
#   CONFIG
# ============================================================
BOT_TOKEN = os.getenv("8934734495:AAGVXUK0muIIPK2XYJhzxwHJoaZNbysc-UY", "")
RENDER_URL = os.getenv("RENDER_EXTERNAL_URL", "")
PORT = int(os.getenv("PORT", 10000))
ZALO_PHONE = "0372834763"
ZALO_URL = f"https://zalo.me/{ZALO_PHONE}"
TIKTOK_URL = os.getenv("TIKTOK_URL", "https://www.tiktok.com/@gai.xinh.vn")
SECRET_TOKEN = os.getenv("SECRET_TOKEN", "LEMINH_TOOL_VIP_2026_KEY")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

LINE = "─────────────"


# ============================================================
#   AUTO DETECT HASH TYPE
# ============================================================
def detect_hash_type(h: str):
    h = h.strip()
    if re.fullmatch(r"[a-fA-F0-9]{32}", h):
        return "MD5"
    if re.fullmatch(r"[a-fA-F0-9]{64}", h):
        return "SHA-256"
    return None


# ============================================================
#   THUẬT TOÁN VIP v7 - 30 VÒNG + 8 LỚP MIX
# ============================================================
def hash_to_score(h: str, htype: str) -> int:
    h = h.lower()

    # LỚP 1: Weight động
    weight = 41 if htype == "MD5" else 53

    # LỚP 2: 6 nguồn entropy
    salt1 = "LEMINH_VIP_2026_V7"
    salt2 = f"SEED_{len(h)}_{weight}"
    salt3 = "X9K2M7P4Q1"
    salt4 = f"ROUND_{hashlib.md5(h.encode()).hexdigest()[:8]}"
    salt5 = "ZK3L8N5W2Y7"

    mixed = (
        f"{h}::{SECRET_TOKEN}::{salt1}::{salt2}::{salt3}::{salt4}::{salt5}"
    ).encode()

    # LỚP 3: Băm 30 vòng xen kẽ 4 hash
    for i in range(30):
        r = i % 4
        if r == 0:
            mixed = hashlib.sha512(mixed + str(i).encode() + salt1.encode()).digest()
        elif r == 1:
            mixed = hashlib.sha256(mixed + str(i).encode() + salt2.encode()).digest()
        elif r == 2:
            mixed = hashlib.blake2b(mixed + str(i).encode() + salt3.encode()).digest()
        else:
            mixed = hashlib.sha3_256(mixed + str(i).encode() + salt4.encode()).digest()

    # LỚP 4: Avalanche - đảo bit 2 lần
    bits = int.from_bytes(mixed[:8], "big")
    bits = ((bits << 13) | (bits >> 51)) & 0xFFFFFFFFFFFFFFFF
    bits ^= 0xA5A5A5A5A5A5A5A5
    bits = ((bits << 7) | (bits >> 57)) & 0xFFFFFFFFFFFFFFFF
    mixed = bits.to_bytes(8, "big") + mixed[8:]

    # LỚP 5: Khuếch tán phi tuyến 3 lớp
    score = 0
    for i in range(0, len(mixed), 2):
        cb = mixed[i:i + 4]
        if len(cb) < 4:
            cb += b"\x00" * (4 - len(cb))
        chunk = int.from_bytes(cb, "big")
        score = (score * weight + (chunk * chunk) % 9973 + chunk) % 100
        score = (score ^ (chunk % 97)) % 100
        inv = pow(chunk % 89 + 1, 87, 89)
        score = (score + inv) % 100

    # LỚP 6: Bit-mix
    final_mix = int.from_bytes(hashlib.sha256(mixed).digest()[:8], "big")
    score = (score * 73 + final_mix) % 100

    # LỚP 7: Modular arithmetic
    score = (score * 97 + 43) % 100

    # LỚP 8: Chuẩn hoá
    return abs(score) % 100


# ============================================================
#   DỰ ĐOÁN
# ============================================================
def predict(h: str) -> dict:
    h = h.strip()
    htype = detect_hash_type(h)
    if not htype:
        return {"error": True}
    score = hash_to_score(h, htype)
    return {
        "hash": h,
        "type": htype,
        "result": "XỈU" if score < 50 else "TÀI",
        "tai": score,
        "xiu": 100 - score,
    }


def esc(t: str) -> str:
    return html.escape(str(t))


# ============================================================
#   HANDLERS
# ============================================================
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = (
        "🎯 <b>LEMINH TOOL MD5</b>\n"
        "Giúp bạn làm giàu thành công 💰\n"
        "Chúc bạn chơi vui vẻ 🎉\n"
        f"{LINE}\n\n"
        "📥 <b>Gửi MD5 (32 ký tự)</b>\n"
        "📥 <b>hoặc HASH (64 ký tự)</b>\n"
        "→ Bot tự nhận diện\n"
        "→ Dự đoán <b>TÀI / XỈU</b>\n\n"
        f"{LINE}\n"
        "🔒 <b>Lệnh ẩn:</b>\n"
        "• /hotro – Zalo + TikTok\n"
        "• /tiktok – TikTok gái xinh\n"
        "• /xoa – Xoá tin nhắn bot"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.HTML)


async def cmd_hotro(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = (
        "📞 <b>HỖ TRỢ - GIẢI TRÍ</b>\n"
        f"{LINE}\n"
        f"• Zalo: <code>{ZALO_PHONE}</code>\n"
        f"• TikTok: {TIKTOK_URL}\n\n"
        "👉 Bấm nút bên dưới"
    )
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("💬 Zalo Hỗ Trợ", url=ZALO_URL)],
        [InlineKeyboardButton("🎵 TikTok Gái Xinh", url=TIKTOK_URL)],
    ])
    await update.message.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=kb)


async def cmd_tiktok(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎵 Mở TikTok", url=TIKTOK_URL)]
    ])
    await update.message.reply_text(
        f"🎵 <b>TIKTOK GÁI XINH</b>\n{LINE}\n{TIKTOK_URL}",
        parse_mode=ParseMode.HTML,
        reply_markup=kb,
    )


async def cmd_xoa(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.delete()
    except Exception:
        pass
    msg = await ctx.bot.send_message(
        chat_id=update.effective_chat.id,
        text="🧹 <b>Đã xoá!</b> Gõ /start để bắt đầu lại.",
        parse_mode=ParseMode.HTML,
    )
    await asyncio.sleep(3)
    try:
        await msg.delete()
    except Exception:
        pass


async def cmd_32(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = (
        "📘 <b>HƯỚNG DẪN 32 KÝ TỰ (MD5)</b>\n"
        f"{LINE}\n"
        "• Chuỗi đúng <b>32</b> ký tự hex\n"
        "• Ví dụ:\n"
        "<code>d41d8cd98f00b204e9800998ecf8427e</code>"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.HTML)


async def cmd_64(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = (
        "📗 <b>HƯỚNG DẪN 64 KÝ T"
Ự (SHA-256)</b       >\n"
        f"{LINE "}\n"
        "• Chuỗi đ27úng <b>64</b> kaeý tự hex\n"
        "• Ví dụ:\n41"
        "<code>e3b0c44298fc1c149afbf4c8996fb924e4649b934ca495991b7852b855</code>"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.HTML)


async def handle_hash(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    res = predict(text)

    if res.get("error"):
        msg = (
            "❌ <b>SAI ĐỊNH DẠNG!</b>\n"
            f"{LINE}\n"
            "• MD5: đúng <b>32</b> ký tự hex (0-9, a-f)\n"
            "• SHA-256: đúng <b>64</b> ký tự hex (0-9, a-f)\n\n"
            "👉 Gõ /32kitu hoặc /64kitu"
        )
        await update.message.reply_text(msg, parse_mode=ParseMode.HTML)
        return

    emoji = "🔴" if res["result"] == "TÀI" else "🔵"
    msg = (
        "★ <b>LEMINH TOOL MD5</b> ★\n"
        f"{LINE}\n"
        f"🔎 <code>{esc(res['hash'])}</code>\n"
        f"🧩 Loại: <b>{esc(res['type'])}</b>\n\n"
        f"{emoji} <b>KẾT QUẢ: {res['result']}</b>\n"
        f"📊 TÀI: <code>{res['tai']}%</code>\n"
        f"📊 XỈU: <code>{res['xiu']}%</code>\n"
        f"{LINE}\n"
        "💰 LEMINH TOOL\n"
        "🎉 Chúc bạn chơi vui vẻ!"
    )
    await update.message.reply_text(msg, parse_mode=ParseMode.HTML)


# ============================================================
#   POST INIT
# ============================================================
async def post_init(app: Application):
    await app.bot.set_my_commands([
        BotCommand("start", "Bắt đầu"),
        BotCommand("32kitu", "Hướng dẫn MD5"),
        BotCommand("64kitu", "Hướng dẫn SHA-256"),
        BotCommand("hotro", "Hỗ trợ Zalo + TikTok"),
        BotCommand("tiktok", "TikTok gái xinh"),
        BotCommand("xoa", "Xoá tin nhắn bot"),
    ])
    await app.bot.delete_webhook(drop_pending_updates=True)
    logger.info("✅ Đã set commands + xoá webhook cũ")


# ============================================================
#   MAIN
# ============================================================
def main():
    if not BOT_TOKEN:
        raise SystemExit("⚠️ Chưa cấu hình BOT_TOKEN!")
    if not RENDER_URL:
        raise SystemExit("⚠️ Thiếu RENDER_EXTERNAL_URL!")

    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("hotro", cmd_hotro))
    app.add_handler(CommandHandler("tiktok", cmd_tiktok))
    app.add_handler(CommandHandler("xoa", cmd_xoa))
    app.add_handler(CommandHandler("32kitu", cmd_32))
    app.add_handler(CommandHandler("64kitu", cmd_64))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_hash))

    webhook_url = f"{RENDER_URL}/{BOT_TOKEN}"
    logger.info(f"🚀 Webhook: {webhook_url}")

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=BOT_TOKEN,
        webhook_url=webhook_url,
        drop_pending_updates=True,
    )


if __name__ == "__main__":
    main()

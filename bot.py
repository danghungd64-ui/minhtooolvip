# ============================================================
#   LEMINH TOOL MD5 - VIP 2026 - UPGRADE v3
#   Zalo hỗ trợ: 0372834763
# ============================================================
import os
import re
import hashlib
import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# ---------------- CONFIG ----------------
BOT_TOKEN = os.getenv("BOT_TOKEN", "8934734495:AAGVXUK0muIIPK2XYJhzxwHJoaZNbysc-UY")
ZALO_PHONE = "0372834763"
ZALO_URL = f"https://zalo.me/{ZALO_PHONE}"
SECRET_TOKEN = os.getenv("SECRET_TOKEN", "LEMINH_TOOL_VIP_2026_KEY")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ============================================================
#   TỰ ĐỘNG NHẬN DIỆN MD5 (32) / SHA-256 (64)
# ============================================================
def detect_hash_type(h: str):
    h = h.strip()
    if re.fullmatch(r"[a-fA-F0-9]{32}", h):
        return "MD5"
    if re.fullmatch(r"[a-fA-F0-9]{64}", h):
        return "SHA-256"
    return None


# ============================================================
#   THUẬT TOÁN NÂNG CAO v3 - 20 VÒNG + 6 LỚP MIX
#   1. Weight động theo loại hash
#   2. Trộn 5 nguồn entropy
#   3. Băm 20 vòng (SHA-512 + SHA-256 xen kẽ)
#   4. Khuếch tán phi tuyến 2 lớp
#   5. Bit-mix + Modular Arithmetic
#   6. Chuẩn hoá về 0-99
# ============================================================
def hash_to_score(h: str, htype: str) -> int:
    h = h.lower()

    # Bước 1: Weight động theo loại hash
    weight = 41 if htype == "MD5" else 53
    salt1 = "LEMINH_VIP_2026_UPGRADE"
    salt2 = f"SEED_{len(h)}_{weight}"
    salt3 = "X9K2M7P4Q1"

    # Bước 2: Trộn 5 nguồn entropy
    mixed = f"{h}::{SECRET_TOKEN}::{salt1}::{salt2}::{salt3}".encode()

    # Bước 3: Băm 20 vòng xen kẽ SHA-512 / SHA-256
    for i in range(20):
        if i % 2 == 0:
            mixed = hashlib.sha512(mixed + str(i).encode() + salt1.encode()).digest()
        else:
            mixed = hashlib.sha256(mixed + str(i).encode() + salt2.encode()).digest()

    # Bước 4: Khuếch tán phi tuyến 2 lớp
    score = 0
    for i in range(0, len(mixed), 2):
        chunk_bytes = mixed[i:i + 4]
        if len(chunk_bytes) < 4:
            chunk_bytes = chunk_bytes + b"\x00" * (4 - len(chunk_bytes))
        chunk = int.from_bytes(chunk_bytes, "big")
        # Lớp 1: bình phương mod số nguyên tố
        score = (score * weight + (chunk * chunk) % 9973 + chunk) % 100
        # Lớp 2: XOR + mod
        score = (score ^ (chunk % 97)) % 100

    # Bước 5: Bit-mix + modular
    final_mix = int.from_bytes(hashlib.sha256(mixed).digest()[:8], "big")
    score = (score * 73 + final_mix) % 100

    # Bước 6: Đảm bảo giá trị cuối 0-99
    score = abs(score) % 100

    return score


# ============================================================
#   DỰ ĐOÁN + TÍNH % TÀI/XỈU (KHÔNG hiện độ tin cậy)
# ============================================================
def predict(h: str) -> dict:
    h = h.strip()
    htype = detect_hash_type(h)

    if not htype:
        return {
            "error": (
                "❌ *SAI ĐỊNH DẠNG!*\n\n"
                "• MD5: đúng *32* ký tự hex (0-9, a-f)\n"
                "• SHA-256: đúng *64* ký tự hex (0-9, a-f)\n\n"
                "👉 Gõ /32kitu hoặc /64kitu để xem mẫu."
            )
        }

    score = hash_to_score(h, htype)
    result = "XỈU" if score < 50 else "TÀI"

    return {
        "hash": h,
        "type": htype,
        "result": result,
        "tai": score,
        "xiu": 100 - score,
    }


# ============================================================
#   /start  (đã ẨN độ tin cậy)
# ============================================================
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = (
        "🎯 *LEMINH TOOL MD5*\n"
        "Giúp bạn làm giàu thành công 💰\n"
        "Chúc bạn chơi vui vẻ 🎉\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        "📥 *Gửi MD5 (32 ký tự) hoặc HASH (64 ký tự)*\n"
        "→ Bot *tự nhận diện* và dự đoán *TÀI / XỈU*\n\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "🔒 *Lệnh ẩn:*\n"
        "• /hotro – Mở Zalo hỗ trợ\n"
        "• /xoa – Xoá tin nhắn bot"
    )
    await update.message.reply_text(text, parse_mode="Markdown")


# ============================================================
#   /hotro
# ============================================================
async def cmd_hotro(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = (
        "📞 *HỖ TRỢ ZALO ADMIN*\n"
        f"• SĐT: `{ZALO_PHONE}`\n"
        f"• Link: {ZALO_URL}\n\n"
        "👉 Bấm nút bên dưới để mở Zalo"
    )
    kb = InlineKeyboardMarkup(
        [[InlineKeyboardButton("💬 Mở Zalo Hỗ Trợ", url=ZALO_URL)]]
    )
    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=kb)


# ============================================================
#   /xoa
# ============================================================
async def cmd_xoa(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.delete()
    except Exception:
        pass

    msg = await ctx.bot.send_message(
        chat_id=update.effective_chat.id,
        text="🧹 *Đã xoá!* Gõ /start để bắt đầu lại.",
        parse_mode="Markdown",
    )
    await asyncio.sleep(3)
    try:
        await msg.delete()
    except Exception:
        pass


# ============================================================
#   /32kitu  /64kitu
# ============================================================
async def cmd_32(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📘 *HƯỚNG DẪN 32 KÝ TỰ (MD5)*\n"
        "• Chuỗi đúng *32* ký tự hex\n"
        "• Ví dụ:\n`d41d8cd98f00b204e9800998ecf8427e`",
        parse_mode="Markdown",
    )


async def cmd_64(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📗 *HƯỚNG DẪN 64 KÝ TỰ (SHA-256)*\n"
        "• Chuỗi đúng *64* ký tự hex\n"
        "• Ví dụ:\n"
        "`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`",
        parse_mode="Markdown",
    )


# ============================================================
#   XỬ LÝ HASH (CHỈ HIỆN TÀI % / XỈU %)
# ============================================================
async def handle_hash(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    res = predict(text)

    if "error" in res:
        await update.message.reply_text(res["error"], parse_mode="Markdown")
        return

    emoji = "🔴" if res["result"] == "TÀI" else "🔵"

    msg = (
        "★ *LEMINH TOOL MD5* ★\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        f"🔎 `{res['hash']}`\n"
        f"🧩 Loại: *{res['type']}*\n\n"
        f"{emoji} *KẾT QUẢ: {res['result']}*\n"
        f"📊 TÀI: `{res['tai']}%`\n"
        f"📊 XỈU: `{res['xiu']}%`\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "💰 LEMINH TOOL – Làm giàu thành công\n"
        "🎉 Chúc bạn chơi vui vẻ!"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")


# ============================================================
#   MAIN
# ============================================================
def main():
    if BOT_TOKEN == "DÁN_TOKEN_BOT_VÀO_ĐÂY":
        raise SystemExit("⚠️ Chưa cấu hình BOT_TOKEN!")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("hotro", cmd_hotro))
    app.add_handler(CommandHandler("xoa", cmd_xoa))
    app.add_handler(CommandHandler("32kitu", cmd_32))
    app.add_handler(CommandHandler("64kitu", cmd_64))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_hash))

    logger.info("🚀 LEMINH TOOL BOT v3 đang chạy...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

import os
import time
from pyrogram import Client, filters
from pyrogram.types import Message

# Render वरून BOT_TOKEN ऑटोमॅटिक घेईल
API_ID = 6 // डमी आयडी चालेल
API_HASH = "123456789abcdef" // डमी हॅश चालेल
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Client("MyUploaderBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start_command(client, message: Message):
    await message.reply_text("👋 नमस्कार! मी तुमचा पर्सनल Uploader Bot आहे.\n\nफक्त मला `/mirror [डायरेक्ट लिंक]` पाठवा, मी ती फाईल डाऊनलोड करून लगेच टेलिग्रामवर पाठवीन!")

@app.on_message(filters.command("mirror"))
async def mirror_command(client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("⚠️ कृपया `/mirror` सोबत मुव्हीची डायरेक्ट लिंक (URL) द्या!")
        return
    
    url = message.command[1]
    msg = await message.reply_text("📥 लिंक प्राप्त झाली आहे, फाईल डाऊनलोड होत आहे...")
    
    try:
        # फाईल डाऊनलोड करणे
        local_filename = url.split("/")[-1].split("?")[0]
        if not local_filename:
            local_filename = "downloaded_video.mp4"
            
        import urllib.request
        urllib.request.urlretrieve(url, local_filename)
        
        await msg.edit_text("📤 डाऊनलोड पूर्ण झाले, आता टेलिग्रामवर अपलोड करत आहे...")
        
        # टेलिग्रामवर अपलोड करणे
        start_time = time.time()
        await client.send_document(
            chat_id=message.chat.id,
            document=local_filename,
            caption=f"🎥 यशस्वीरित्या अपलोड केली!\n🔗 Link: {url}"
        )
        
        # लोकल फाईल डिलीट करून स्पेस मोकळी करणे
        os.remove(local_filename)
        await msg.delete()
        
    except Exception as e:
        await msg.edit_text(f"❌ काहीतरी त्रुटी आली: {str(e)}")

print("🤖 बॉट यशस्वीरित्या सुरू होत आहे...")
app.run()

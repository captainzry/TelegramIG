from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, JobQueue, Job
import requests
import asyncio

# Function to handle the /hello command
async def hello(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

# Function to check the username status
async def check_username_status(context: CallbackContext, username: str, chat_id: int) -> bool:
    try:
        url = 'https://i.instagram.com/accounts/account_recovery_send_ajax/?hl=en'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'X-Csrftoken': 'missing',
            'X-Ig-App-Id': '936619743392459',
            'X-Instagram-Ajax': 'fb9c41d1e1fd',
            'X-Requested-With': 'XMLHttpRequest',
            'X-Asbd-Id': '129477',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Ig-Www-Claim': '0'
        }
        data = {'email_or_username': username}
        req = requests.post(url=url, headers=headers, data=data)
        response = req.text

        if "No users found" in response:
            return False
        elif "email_or_sms_sent" in response or "Email Sent" in response:
            await context.bot.send_message(chat_id=chat_id, text=f"✅ Successfully active user {[username]}")
            return True
        else:
            await context.bot.send_message(chat_id=chat_id, text=response)
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

# Function to handle the /check_username command
async def check_username(update: Update, context: CallbackContext) -> None:
    args = context.args
    if args:
        username = args[0]
        chat_id = update.message.chat_id
        
        if await check_username_status(context, username, chat_id):  # Check username immediately
            return  # Stop the execution if username is alive
        
        while True:
            await asyncio.sleep(200)  
            if await check_username_status(context, username, chat_id):  # Check username again
                break  # Stop the loop if username is alive
    else:
        await update.message.reply_text("Please provide a username to check.")

# Initialize the bot application
app = ApplicationBuilder().token("7052876472:AAFpgLGLAPWIEyKoGCs5jgeNnRoA9w2aNDA").build()

# Add command handlers
app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("unban", check_username))

# Run the bot
app.run_polling()

import subprocess
import os
from telethon.sync import TelegramClient, events

# Telegram API credentials
api_id = '28811360'
api_hash = '62df1732bba44f40f37bcdcbe78e22be'
phone_number = '+923094712571'

# Path to save the captured image
IMAGE_PATH = './captured_image.jpg'

# Function to handle the '/hi' command
async def hi_command_handler(event):
    # Capture an image using ffmpeg
    subprocess.call(['ffmpeg', '-f', 'v4l2', '-video_size', '640x480', '-i', '/dev/video0', '-vframes', '1', IMAGE_PATH])

    # Check if the captured image exists
    if os.path.exists(IMAGE_PATH):
        # Send the captured image to Telegram
        await event.respond(file=IMAGE_PATH)
    else:
        await event.respond("Failed to capture the image.")

# Create the Telegram client
client = TelegramClient(phone_number, api_id, api_hash)

# Register the event handler for the '/hi' command
@client.on(events.NewMessage())
async def event_handler(event):
    await hi_command_handler(event)
    os.remove(IMAGE_PATH)

# Start the Telegram client
client.start()
client.run_until_disconnected()

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import logging
from typing import Final
import requests
import inputText
import random
# Your bot token from BotFather
TOKEN: Final = '6730306930:AAHf6Fo3i8wWmFZ0K2dG88SnjU54J_FX-ME'
BOT_USERNAME:Final = '@DepDect1_bot'
API_KEY:Final = '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'

recommendations = [
    "Take a short walk in nature. Even a few minutes can help clear your mind and boost your mood.",
    "Write down your thoughts in a journal. Expressing what you're going through can be a therapeutic outlet.",
    "Practice mindfulness or meditation. These practices can help you stay grounded and focused on the present.",
    "Reach out to a friend or loved one. Connecting with others can provide support and reduce feelings of isolation.",
    "Engage in a creative activity, such as drawing, painting, or playing music. Creative expression can be a powerful way to convey emotions.",
    "Try gentle exercise, like yoga or stretching. Physical activity can release endorphins, which are natural mood lifters.",
    "Set one small, achievable goal for the day. Accomplishing it can give you a sense of progress and purpose.",
    "Limit your intake of alcohol and caffeine. Both can affect your mood and energy levels.",
    "Ensure you're getting enough sleep. Poor sleep can exacerbate feelings of depression.",
    "Consider volunteering. Helping others can improve your sense of worth and connect you with your community."
]

last_user_messages ='none' 

#commands:
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Greet the user and instruct them
    await update.message.reply_text('Hello! Send me a message, I will try to help you.')

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Greet the user and instruct them
    await update.message.reply_text('I will help you understand your feelings, just text me.')
async def analyze_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    detection: str = inputText.predict_depression(last_user_messages)  # Assuming this is your prediction function
    # Reply based on the detection
    await update.message.reply_text(f'Your messages indicates a: {detection} behavior')
        
    if detection == 'Depressive':  # Assuming 'Depressive' is a possible output of predict_depression
        random_recommendation = random.choice(recommendations)
        await update.message.reply_text(f'Here is something you might try: {random_recommendation}')
    else:
        await update.message.reply_text(f'You are doing just fine, keep going!')
    

#Responses:
def handle_response(text: str):
    processes: str=text.lower()
    detection: str = inputText.predict_depression(text)  # Assuming this is your prediction function

    if 'hello'  in processes:
        return 'hi there, how are you today?'
    if 'lonely' in processes:
        return 'would you like to tell me about it?'
    if 'how are you?' in processes:
        return 'Im fine,how are you doing? '
    if 'help' in processes:
        return 'i will try to help you as much as I can'
    if 'trip' in processes:
        return 'Im so glad to hear about it?'
    if 'thank you' in processes:
        return 'glad to help.I m here any time you need.'

    if detection=="Depressive":#found a depressive behavior
        random_recommendation = random.choice(recommendations)
        ret_str = ('Your messages indicates a depressive behavior\n' 
           'Here is something you might try: \n'
           + random_recommendation)

        return ret_str
    return 'tell me more, I hear you'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    last_user_messages = update.message.text
    message_type: str = update.message.chat.type
    text: str = update.message.text
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    
    response: str = handle_response(text)
    
    print('Bot:', response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f'Update{update}caused error{context.error}')


def main() -> None:
    print('Starting Bot...')
    application = Application.builder().token(TOKEN).build()
    #commands:
    # Add a handler for the /start command
    application.add_handler(CommandHandler('start', start))
    # Add a handler for the /help command
    application.add_handler(CommandHandler('help', help))
    # Add a handler for the /analyze user text command
    application.add_handler(CommandHandler('analyze_text', analyze_text ))
    # Add a handler for text messages that are not commands
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    #Messages:
    application.add_handler(MessageHandler(filters.TEXT,handle_message))
    #Errors:
    application.add_error_handler(error)

    # Start the bot
    print('Polling...')
    application.run_polling(poll_interval=3)#checks every 3 sec if there are new messages

if __name__ == '__main__':
    main()

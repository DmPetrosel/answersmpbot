import json, logging
from aiogram import Bot
from db.get import *
from aiogram.client.default import Default



class MyBot(Bot):
    async def send_messages(self,
                            text,
                                user_list = None,
                            parse_mode = None,
                            entities = None,
                            disable_web_page_preview = None,
                            message_thread_id = None,
                            disable_notification = None,
                            protect_content = None,
                            reply_to_message_id = None,
                            allow_sending_without_reply = None,
                            reply_markup= None):
        """
        Send messages for all users given in config.json (user_list). 
        First positional argument is the text which is mandatory and the rest are optional
        """
        result = []
        if user_list:
            for user in user_list:
                try:
                    result.append(
                    await self.send_message(chat_id=user, text=text, parse_mode = parse_mode,
                                    entities = entities,
                                    disable_web_page_preview = disable_web_page_preview,
                                    message_thread_id = message_thread_id,
                                    disable_notification = disable_notification,
                                    protect_content = protect_content,
                                    reply_to_message_id = reply_to_message_id,
                                    allow_sending_without_reply = allow_sending_without_reply,
                                    reply_markup= reply_markup)
                    )
                except Exception as e:
                    logging.error(f"Error when sending a message to multiple users. {e}")
        return result
    async def send_messages_beside(self,
                                   user_beside,
                            text,
                                user_list = None,
                            parse_mode = None,
                            entities = None,
                            disable_web_page_preview = None,
                            message_thread_id = None,
                            disable_notification = None,
                            protect_content = None,
                            reply_to_message_id = None,
                            allow_sending_without_reply = None,
                            reply_markup= None):
        """
        Send messages for all users given in config.json (user_list). 
        !!!Beside user_beside!!!
        First positional argument is the beside user id second is the text which is mandatory and the rest are optional
        """
        result = []
        if user_list:
            for user in user_list:
                try:
                    if user == user_beside:
                        continue
                    result.append(   
                    await self.send_message(chat_id=user, text=text, parse_mode = parse_mode,
                                    entities = entities,
                                    disable_web_page_preview = disable_web_page_preview,
                                    message_thread_id = message_thread_id,
                                    disable_notification = disable_notification,
                                    protect_content = protect_content,
                                    reply_to_message_id = reply_to_message_id,
                                    allow_sending_without_reply = allow_sending_without_reply,
                                    reply_markup= reply_markup)
                    )
                except Exception as e:
                    logging.error(f"Mostly user {user} not found in config.json or did not press 'start', error: {e}")
        return result
    
    async def edit_messages_beside(self,
        text: str,
        message_beside,
        messages_list,
        business_connection_id  = None,
        chat_id = None,
        
        inline_message_id = None,
        parse_mode = Default("parse_mode"),
        entities = None,
        link_preview_options = Default(
            "link_preview"
        ),
        reply_markup = None,
        disable_web_page_preview = Default(
            "link_preview_is_disabled"
        ),
        request_timeout = None,):
        """
        Send messages for all users given in config.json (user_list). 
        !!!Beside user_beside!!!
        First positional argument is the beside user id second is the text which is mandatory and the rest are optional
        """
        result = []
        if messages_list:
            for mess_id in messages_list:
                try:
                    if mess_id[1] == message_beside:
                        continue
                    result.append(   
                    await self.edit_message_text(text = text,
                                business_connection_id  = business_connection_id,
                                chat_id = int(mess_id[0]),
                                message_id = int(mess_id[1]), # Choosing mess_id instead of message_id
                                inline_message_id = inline_message_id,
                                parse_mode = parse_mode,
                                entities = entities,
                                link_preview_options = link_preview_options,
                                reply_markup = reply_markup,
                                disable_web_page_preview = disable_web_page_preview,
                                request_timeout = request_timeout,)
                                            )
                except Exception as e:
                    logging.error(f"Mostly user {user} not found in config.json or did not press 'start', error: {e}")
        return result
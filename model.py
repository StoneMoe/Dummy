#!/usr/bin/env python
# coding:utf-8
import sys
import json

from config import Config


class Update(object):
    """
    This object represents an incoming update.
    At most one of the optional parameters can be present in any given update.
    """

    # convenients: IS_[UPDATETYPES]

    UPDATE_TYPES = {
        "message": "Message",
        "edited_message": "Message",
        "channel_post": "Message",
        "edited_channel_post": "Message",
        "inline_query": "NotImplemented",
        "chosen_inline_result": "NotImplemented",
        "callback_query": "NotImplemented",
        "shipping_query": "NotImplemented",
        "pre_checkout_query": "NotImplemented"
    }

    def __init__(self, updateJson):
        self._raw    = updateJson
        self._dict   = json.loads(updateJson)

        self.handled = False

        self.id      = self._dict["update_id"]
        self.msg     = None

        # Expose type bools for outside, and load data to model dynamically
        for updateType, ModelClassName in Update.UPDATE_TYPES.items():
            if updateType in self._dict:
                if ModelClassName is "NotImplemented":
                    raise NotImplementedError("UpdateType '%s' is not implemented yet" % updateType)
                modelClass = getattr(sys.modules[__name__], ModelClassName)
                self.msg = modelClass(self._dict[updateType])
                setattr(self, "IS_" + updateType.upper().replace("_", ""), True)
            else:
                setattr(self, "IS_" + updateType.upper().replace("_", ""), False)

        if self.msg is None:
            raise NotImplementedError("Cannot identify UpdateInnerBody")


class Message(object):
    """This object represents a message."""

    # convenients: HAS_[MESSAGETYPES], IS_MASTER, IS_MENTIONED

    MESSAGE_TYPES = [  # convenient message types, but not covered all message types  ## HOW TO: use HAS_[Type], like if msg.HAS_AUDIO:
        "text",
        "audio",
        "document",
        "game",
        "photo",
        "sticker",
        "video",
        "voice",
        "video_note",
        "caption",
        "contact",
        "location",
        "venue",
        "new_chat_members",
        "left_chat_member",
        "new_chat_title",
        "new_chat_photo",
        "delete_chat_photo",
        "pinned_message"
    ]

    def __init__(self, messageDict):
        # Expose message bools for outside
        # Generate from original data before deflate
        for msgType in Message.MESSAGE_TYPES:
            setattr(
                self,
                "HAS_" + msgType.upper().replace("_", ""),
                msgType in messageDict
            )

        self._dict = Message.deflate(messageDict)

        self.id = self._dict["message_id"]
        self.sendTime = self._dict["date"]
        self.chat = Chat(self._dict["chat"])

        # Optional
        self.sender          = User(self._dict["from"]) if self._dict["from"] else None
        self.forwarded       = self._dict["forward_date"]
        self.forwardFrom     = User(self._dict["forward_from"]) if self._dict["forward_from"] else None
        self.reply           = Message(self._dict["reply_to_message"]) if self._dict["reply_to_message"] else None
        self.editTime        = self._dict["edit_date"]
        self.text            = self._dict["text"].replace("@%s" % Config.botUsername, "") if self._dict["text"] else None
        self.audio           = self._dict["audio"]
        self.document        = self._dict["document"]
        self.game            = self._dict["game"]
        self.photo           = self._dict["photo"]
        self.sticker         = self._dict["sticker"]
        self.video           = self._dict["video"]
        self.voice           = self._dict["voice"]
        self.videoNote       = self._dict["video_note"]
        self.caption         = self._dict["caption"]
        self.contact         = self._dict["contact"]
        self.location        = self._dict["location"]
        self.venue           = self._dict["venue"]
        self.newChatMembers  = self._dict["new_chat_members"]
        self.leftChatMember  = self._dict["left_chat_member"]
        self.newChatTitle    = self._dict["new_chat_title"]
        self.newChatPhoto    = self._dict["new_chat_photo"]
        self.deleteChatPhoto = self._dict["delete_chat_photo"]
        self.pinnedMessage   = self._dict["pinned_message"]

        # convenient variables
        self.IS_MENTIONED = True if self.HAS_TEXT and "@%s" % Config.botUsername in self._dict["text"] else False
        self.IS_MASTER    = True if self.sender and self.sender.id == Config.botMasterID else False

    @staticmethod
    def deflate(messageDict):
        messageDict.setdefault("from", None)
        messageDict.setdefault("forward_from", None)
        messageDict.setdefault("forward_from_chat", None)
        messageDict.setdefault("forward_from_message_id", None)
        messageDict.setdefault("forward_signature", None)
        messageDict.setdefault("forward_date", None)
        messageDict.setdefault("reply_to_message", None)
        messageDict.setdefault("edit_date", None)
        messageDict.setdefault("author_signature", None)
        messageDict.setdefault("text", None)
        messageDict.setdefault("entities", None)
        messageDict.setdefault("caption_entities", None)
        messageDict.setdefault("audio", None)
        messageDict.setdefault("document", None)
        messageDict.setdefault("game", None)
        messageDict.setdefault("photo", None)
        messageDict.setdefault("sticker", None)
        messageDict.setdefault("video", None)
        messageDict.setdefault("voice", None)
        messageDict.setdefault("video_note", None)
        messageDict.setdefault("caption", None)
        messageDict.setdefault("contact", None)
        messageDict.setdefault("location", None)
        messageDict.setdefault("venue", None)
        messageDict.setdefault("new_chat_members", None)
        messageDict.setdefault("left_chat_member", None)
        messageDict.setdefault("new_chat_title", None)
        messageDict.setdefault("new_chat_photo", None)
        messageDict.setdefault("delete_chat_photo", None)
        messageDict.setdefault("group_chat_created", None)
        messageDict.setdefault("supergroup_chat_created", None)
        messageDict.setdefault("channel_chat_created", None)
        messageDict.setdefault("migrate_to_chat_id", None)
        messageDict.setdefault("migrate_from_chat_id", None)
        messageDict.setdefault("pinned_message", None)
        messageDict.setdefault("invoice", None)
        messageDict.setdefault("successful_payment", None)
        return messageDict


class Chat(object):
    """This object represents a chat."""

    # convenients: IS_[CHATTYPES]

    CHAT_TYPES = [
        "private",
        "group",
        "supergroup",
        "channel"
    ]

    def __init__(self, ChatDict):
        self._dict = Chat.deflate(ChatDict)

        self.id = self._dict["id"]

        # Optional
        self.title = self._dict["title"]

        # Expose chatType bools for outside
        for chatType in Chat.CHAT_TYPES:
            setattr(
                self,
                "IS_" + chatType.upper().replace("_", ""),
                self._dict["type"] == chatType
            )

    @staticmethod
    def deflate(ChatDict):
        ChatDict.setdefault("title", None)
        ChatDict.setdefault("username", None)
        ChatDict.setdefault("first_name", None)
        ChatDict.setdefault("last_name", None)
        ChatDict.setdefault("all_members_are_administrators", None)
        ChatDict.setdefault("photo", None)
        ChatDict.setdefault("description", None)
        ChatDict.setdefault("invite_link", None)
        ChatDict.setdefault("pinned_message", None)
        ChatDict.setdefault("sticker_set_name", None)
        ChatDict.setdefault("can_set_sticker_set", None)
        return ChatDict


class User(object):
    """This object represents a Telegram user or bot."""
    def __init__(self, UserDict):
        self._userDict = User.deflate(UserDict)

        self.id = self._userDict["id"]
        self.isBot = self._userDict["is_bot"]
        self.nickname = "%s %s" % (self._userDict["first_name"], self._userDict["last_name"]) if self._userDict["last_name"] else self._userDict["first_name"]
        self.username = self._userDict["username"]

    @staticmethod
    def deflate(UserDict):
        UserDict.setdefault("last_name", None)
        UserDict.setdefault("username", None)
        UserDict.setdefault("language_code", None)
        return UserDict

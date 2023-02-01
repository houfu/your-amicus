"""
Chat component for Web App
"""
import datetime

import pynecone as pc

from your_amicus.chains import DefaultChain
from your_amicus.state import State


class Message(pc.Base):
    text: str
    sent_time: str
    outgoing: bool


def get_result(prompt: str) -> str:
    llm = DefaultChain()
    result = llm.predict(prompt=prompt).strip()
    return result


class ChatState(State):
    input_message: str
    messages: list[Message] = []
    is_waiting: bool = False

    def handle_new_message(self):
        self.messages.append(Message(text=self.input_message, outgoing=True, sent_time=str(datetime.datetime.now())))
        self.messages = self.messages
        print(self.messages[-1])
        self.is_waiting = True
        prompt = self.input_message
        self.input_message = ""
        self.messages.append(Message(text=get_result(prompt), outgoing=False,
                                     sent_time=str(datetime.datetime.now())))
        self.messages = self.messages
        self.is_waiting = False


def render_message(message: Message, index):
    return pc.cond(
        message.outgoing,
        pc.flex(
            pc.flex(
                pc.text(message.message),
                bg="black", color="white", minW="100px", maxW="350px", my="1", p="3"
            ),
            key=index, w="100%", justify="flex-end"
        ),
        pc.flex(
            pc.avatar(ame='Your Amicus', src="android-chrome-192x192.png"),
            pc.flex(
                pc.text(message.message),
                bg="black", color="white", minW="100px", maxW="350px", my="1", p="3"
            ),
            key=index, w="100%"
        )
    )


def message_list():
    return pc.flex(
        pc.foreach(
            ChatState.messages, render_message
        ),
        pc.cond(
            ChatState.is_waiting,
            pc.circular_progress(is_indeterminate=True)
        ),
        width="100%", height="80%",
        padding="3", overflow_y="scroll", direction="column"
    )


def message_input():
    return pc.flex(
        pc.input(
            placeholder="Type Something...",
            border="none", border_radius="none",
            on_blur=ChatState.set_input_message,
        ),
        pc.button(
            "Send",
            bg="black", color="white",
            disabled=ChatState.is_waiting,
            on_click=ChatState.handle_new_message
        ),
        width="100%", margin_top="5px"
    )


def header():
    return pc.flex(
        pc.avatar(
            pc.avatar_badge(box_size="1em", bg="green"),
            name='Your Amicus', size='lg', src="android-chrome-192x192.png"
        ),
        pc.flex(
            pc.text("Your Amicus", font_size="lg", font_weight="bold"),
            pc.text("Online", color="green"),
            direction="column", margin="5", justify="center"
        )
    )


def chat():
    return pc.flex(
        pc.flex(
            header(),
            pc.divider(),
            message_list(),
            pc.divider(),
            message_input(),
            direction="column",
            width=["95%", "95%", "75%", "75%", "40%"], height="90%"
        ),
        width="100%",
        height="90vh",
        justify="center",
        align="center"
    )

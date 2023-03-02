"""
Chat component for Web App
"""
import datetime

import pynecone as pc

from your_amicus.state import State


class Message(pc.Model, table=True):
    user: str
    text: str
    sent_time: float = datetime.datetime.now().timestamp()
    outgoing: str


def get_result(prompt: str) -> str:
    # llm = DefaultChain()
    # result = llm.predict(prompt=prompt).strip()
    import time
    time.sleep(1.5)
    return f"I hear you! You said '{prompt}'"


class ChatState(State):
    input_message: str
    is_waiting: bool = False
    user: int = 1
    messages: list[Message] = [
        Message(text="Hello there! This is the Amicus. I am here to help. Let's talk!", user=1, outgoing="Amicus")]

    def toggle_is_waiting(self):
        self.is_waiting = not self.is_waiting

    def clear_input(self):
        self.input_message = ""

    def save_outgoing_message(self):
        if self.input_message != "":
            self.messages = self.messages + [Message(text=self.input_message, outgoing="You", user=self.user)]

    def save_incoming_message(self):
        if self.input_message != "":
            self.messages = self.messages + [
                Message(text=get_result(self.input_message), outgoing="Amicus", user=self.user)]

    def set_input(self, value):
        self.input_message = value


def message_list():
    def render_message(message: Message, index):
        amicus_message = pc.list_item(
            pc.flex(
                pc.text(message.text),
                bg="black", color="white", minW="100px", maxW="350px", my="1", p="3"
            ),
            key=index, w="100%", justifyContent="flex-start", display="flex"
        )
        your_message = pc.list_item(
            pc.flex(
                pc.text(message.text),
                bg="blue", color="white", minW="100px", maxW="350px", my="1", p="3"
            ),
            key=index, w="100%", justifyContent="flex-end", display="flex"
        )
        return pc.cond(
            message.outgoing == "Amicus",
            amicus_message,
            your_message
        )

    return pc.flex(
        pc.list(
            pc.foreach(
                ChatState.messages, render_message
            )
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
            on_click=[
                ChatState.save_outgoing_message,
                ChatState.toggle_is_waiting,
                ChatState.save_incoming_message,
                ChatState.clear_input,
                ChatState.toggle_is_waiting,
            ]
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
            width="100%", height="100%"
        ),
        width="100%",
        height="90vh",
        justify="center",
        align="center"
    )

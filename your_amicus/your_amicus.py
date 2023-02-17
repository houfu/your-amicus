import pynecone as pc

from your_amicus.chat import chat
from your_amicus.helpers import navbar
from your_amicus.state import State


def home():
    return pc.center(
        pc.vstack(
            pc.center(
                chat(),
                width="100%",
            ),
            width=["95%", "80%", "80%", "50%", "50%"],
            spacing="2em",
            background="white",
        ),
        margin_top="1em",
        text_align="top",
        position="relative",
        width="100%",
    )


def index():
    return pc.box(
        pc.vstack(
            navbar(),
            home(),
        ),
        padding_top="5em",
        text_align="top",
        position="relative",
        width="100%",
        height="100vh",
        background="url(background-notebook.webp) repeat-y"
    )


# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index,
             title="Your Amicus -- Your Robot Lawyer Friend",
             description="Chat with Your Amicus to tap on his legal knowledge and helpfulness",
             image="android-chrome-192x192.png",
             )
app.add_page(home)
app.compile()

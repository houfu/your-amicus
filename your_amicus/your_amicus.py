import pynecone as pc

from your_amicus.helpers import navbar


class State(pc.State):
    """The app state."""

    prompt: str = ""
    result: str = "Ask a question and see what is your Amicus response."

    is_waiting_for_LLM: bool = False

    def toggle_waiting(self):
        self.is_waiting_for_LLM = not self.is_waiting_for_LLM

    async def get_result(self):
        self.result = ""
        from your_amicus.chains import DefaultChain
        llm = DefaultChain()
        result = llm.predict(prompt=self.prompt)
        self.result = result.strip()


def home():
    return pc.center(
        pc.vstack(
            pc.center(
                pc.vstack(
                    pc.heading("Ask Your Amicus", font_size="1.5em"),
                    pc.text_area(
                        on_blur=State.set_prompt, placeholder="Question", width="100%"
                    ),
                    pc.button("Get Answer", on_click=[State.toggle_waiting, State.get_result, State.toggle_waiting],
                              width="100%",
                              is_loading=State.is_waiting_for_LLM),
                    pc.text(State.result, width="100%"),
                    shadow="lg",
                    padding="1em",
                    border_radius="20px 20px 20px 20px",
                    width="100%",
                ),
                width="100%",
            ),
            width=["95%", "80%", "80%", "50%", "50%"],
            spacing="2em",
            background="white",
        ),
        padding_top=["1em", "1em", "1em", "6em", "6em"],
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
             title="Your Amicus -- Your Robot Lawyer Fried",
             description="Chat with Your Amicus to tap on his legal knowledge and helpfulness",
             image="android-chrome-192x192.png",
             )
app.add_page(home)
app.compile()

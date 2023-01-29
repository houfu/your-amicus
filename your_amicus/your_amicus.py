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
                    border_radius="lg",
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
        background="radial-gradient(circle at 22% 11%,rgba(62, 180, 137,.20),hsla(0,0%,100%,0) 19%),radial-gradient(circle at 82% 25%,rgba(33,150,243,.18),hsla(0,0%,100%,0) 35%),radial-gradient(circle at 25% 61%,rgba(250, 128, 114, .28),hsla(0,0%,100%,0) 55%)",
    )


# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index)
app.add_page(home)
app.compile()

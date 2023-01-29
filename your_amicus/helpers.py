import pynecone as pc


def navbar():
    return pc.box(
        pc.hstack(
            pc.link(
                pc.hstack(
                    pc.image(src="apple-touch-icon.png", height="45px", width="auto"),
                    pc.heading("Your Amicus")),
                href="/"
            ),
            pc.menu(
                pc.menu_button(
                    "Menu"
                ),
                pc.menu_list(
                    pc.link(pc.menu_item("About Your Amicus"), href="/about"),
                ),
            ),
            justify="space-between",
            alignItems="center",
            border_bottom="0.2em solid #F0F0F0",
            padding_x="2em",
            padding_y="1em",
            bg="rgba(255,255,255, 0.90)",
        ),
        position="fixed",
        width="100%",
        top="0px",
        z_index="500",
    )

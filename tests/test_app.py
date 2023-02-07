import pynecone as pc


def test_app():
    from your_amicus.your_amicus import State
    app = pc.App(state=State)
    assert app

    from your_amicus.your_amicus import index
    app.add_page(index)
    from your_amicus.your_amicus import home
    app.add_page(home)
    assert set(app.pages.keys()) == {"index", "home"}

import {useEffect, useRef, useState} from "react"
import {useRouter} from "next/router"
import {connect, E, updateState} from "/utils/state"
import "focus-visible/dist/focus-visible"
import {
    Box,
    Button,
    Center,
    Heading,
    HStack,
    Image,
    Link,
    Menu,
    MenuButton,
    MenuItem,
    MenuList,
    Text,
    Textarea,
    VStack
} from "@chakra-ui/react"
import NextLink from "next/link"
import NextHead from "next/head"

const EVENT = "wss://None-your_amicus.api.pynecone.app/event"
export default function Component() {
    const [state, setState] = useState({
        "is_waiting_for_LLM": false,
        "prompt": "",
        "result": "Ask a question and see what is your Amicus response.",
        "events": [{"name": "state.hydrate"}]
    })
    const [result, setResult] = useState({"state": null, "events": [], "processing": false})
    const router = useRouter()
    const socket = useRef(null)
    const {isReady} = router;
    const Event = events => setState({
        ...state,
        events: [...state.events, ...events],
    })
    useEffect(() => {
        if (!isReady) {
            return;
        }
        if (!socket.current) {
            connect(socket, state, setState, result, setResult, router, EVENT)
        }
        const update = async () => {
            if (result.state != null) {
                setState({
                    ...result.state,
                    events: [...state.events, ...result.events],
                })
                setResult({
                    state: null,
                    events: [],
                    processing: false,
                })
            }
            await updateState(state, setState, result, setResult, router, socket.current)
        }
        update()
    })
    return (
        <Box sx={{
            "paddingTop": "5em",
            "textAlign": "top",
            "position": "relative",
            "width": "100%",
            "height": "100vh",
            "background": "radial-gradient(circle at 22% 11%,rgba(62, 180, 137,.20),hsla(0,0%,100%,0) 19%),radial-gradient(circle at 82% 25%,rgba(33,150,243,.18),hsla(0,0%,100%,0) 35%),radial-gradient(circle at 25% 61%,rgba(250, 128, 114, .28),hsla(0,0%,100%,0) 55%)"
        }}><VStack><Box sx={{"position": "fixed", "width": "100%", "top": "0px", "zIndex": "500"}}><HStack
            justify="space-between"
            sx={{
                "borderBottom": "0.2em solid #F0F0F0",
                "paddingX": "2em",
                "paddingY": "1em",
                "bg": "rgba(255,255,255, 0.90)"
            }}><NextLink passHref={true}
                         href="/"><Link><HStack><Image src="favicon.ico"/>
            <Heading>{`Your Amicus`}</Heading></HStack></Link></NextLink>
            <Menu><MenuButton>{`Menu`}</MenuButton>
                <MenuList><NextLink passHref={true}
                                    href="/about"><Link><MenuItem>{`About Your Amicus`}</MenuItem></Link></NextLink></MenuList></Menu></HStack></Box>
            <Center sx={{
                "paddingTop": ["1em", "1em", "1em", "6em", "6em"],
                "textAlign": "top",
                "position": "relative",
                "width": "100%"
            }}><VStack spacing="2em"
                       sx={{"width": ["95%", "80%", "80%", "50%", "50%"], "background": "white"}}><Center
                sx={{"width": "100%"}}><VStack
                sx={{"shadow": "lg", "padding": "1em", "borderRadius": "lg", "width": "100%"}}><Heading
                sx={{"fontSize": "1.5em"}}>{`Ask Your Amicus`}</Heading>
                <Textarea placeholder="Question"
                          onBlur={(_e) => Event([E("state.set_prompt", {value: _e.target.value})])}
                          sx={{"width": "100%"}}/>
                <Button isLoading={state.is_waiting_for_LLM}
                        onClick={() => Event([E("state.toggle_waiting", {}), E("state.get_result", {}), E("state.toggle_waiting", {})])}
                        sx={{"width": "100%"}}>{`Get Answer`}</Button>
                <Text sx={{"width": "100%"}}>{state.result}</Text></VStack></Center></VStack></Center></VStack>
            <NextHead><title>{`Pynecone App`}</title>
                <meta content="A Pynecone app."
                      name="description"/>
                <meta property="og:image"
                      content="favicon.ico"/>
            </NextHead></Box>
    )
}
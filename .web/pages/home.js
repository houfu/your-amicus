import {useEffect, useRef, useState} from "react"
import {useRouter} from "next/router"
import {connect, E, updateState} from "/utils/state"
import "focus-visible/dist/focus-visible"
import {Button, Center, Heading, Text, Textarea, VStack} from "@chakra-ui/react"
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
            <Text sx={{"width": "100%"}}>{state.result}</Text></VStack></Center></VStack>
            <NextHead><title>{`Pynecone App`}</title>
                <meta content="A Pynecone app."
                      name="description"/>
                <meta property="og:image"
                      content="favicon.ico"/>
            </NextHead></Center>
    )
}
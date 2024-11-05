"use client"
import Editor from "@/components/editor/Editor";
import {useSelector} from "react-redux";
import {selectSession} from "@/store/slices/projectSlice";

export default function EditorContainer() {

    const session = useSelector(selectSession)

    return <Editor userSession={session.userSession} headerTitle={session.project.name}/>

}
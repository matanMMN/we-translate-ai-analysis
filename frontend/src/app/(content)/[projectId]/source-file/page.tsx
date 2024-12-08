import {fetchProjectRefOrSrc} from "@/actions/fetchProjectFile";
import SourceFile from "@/components/source-file/SourceFile";

export default async function ReferenceFilePage({params}: {
    params: Promise<{ projectId: string }>
}) {

    const {projectId} = await params
    const refFile: File | null = await fetchProjectRefOrSrc(projectId, 'source')

    return (
        <div className="max-h-[calc(100dvh-300px)]">
            <SourceFile file={refFile}/>
        </div>
    )
}
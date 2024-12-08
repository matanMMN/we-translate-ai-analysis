import ReferenceFile from "@/components/reference-file/ReferenceFile";
import {fetchProjectRefOrSrc} from "@/actions/fetchProjectFile";

export default async function ReferenceFilePage({params}: {
    params: Promise<{ projectId: string }>
}) {

    const {projectId} = await params
    const refFile: File | null = await fetchProjectRefOrSrc(projectId, 'reference')

    return (
        <div className="max-h-[calc(100dvh-300px)]">
            <ReferenceFile file={refFile}/>
        </div>
    )
}
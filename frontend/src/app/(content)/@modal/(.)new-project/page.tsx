import Modal from "@/components/Modal";
import NewProjectForm from "@/components/newProjectForm/NewProjectForm";
import {ErrorBoundary} from '@/components/newProjectForm/ErrorBoundary';

export default function InterceptedNewProjectPage() {
    return (
        <Modal>
            <div className="w-full max-w-md mx-auto">
                <ErrorBoundary>
                    <NewProjectForm/>
                </ErrorBoundary>
            </div>
        </Modal>
    )
}
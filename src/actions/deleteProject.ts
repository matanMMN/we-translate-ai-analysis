'use server'


export async function deleteProject(projectId: string, accessToken: string): Promise<boolean> {
    try {

        const res = await fetch(`http://localhost:8000/jobs/${projectId}`, {
            method: 'DELETE',
            headers: {
                'accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            }
        });
        console.log(res)
        if (res.status === 200)
            return true;
        else throw new Error("Failed to delete project")
        // Get the path to userData.json
        // const filePath = path.join(process.cwd(), 'src', 'data', 'userData.json');
        //
        // // Read the current data
        // const fileContent = await fs.readFile(filePath, 'utf8');
        // const projects = JSON.parse(fileContent);
        //
        // // Find the project index
        // const projectIndex = projects.findIndex((project: any) => project.id === projectId);
        //
        // if (projectIndex === -1) {
        //     throw new Error('Project not found');
        // }
        //
        // // Remove the project
        // projects.splice(projectIndex, 1);
        //
        // // Write the updated data back to the file
        // await fs.writeFile(filePath, JSON.stringify(projects, null, 2), 'utf8');

    } catch (error) {
        console.error('Error deleting project:', error);
        return false;
    }
} 
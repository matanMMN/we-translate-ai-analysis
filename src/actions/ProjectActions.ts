'use server'

import { revalidatePath } from 'next/cache'
import { Project } from '@/lib/userData'
import {getUser} from "@/lib/AuthGuard";

// async function uploadFileToBackend(file: File): Promise<string> {
//   const formData = new FormData()
//   formData.append('file', file)
//
//   const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/upload`, {
//     method: 'POST',
//     body: formData,
//   })
//
//   if (!response.ok) {
//     throw new Error('Failed to upload file')
//   }
//
//   const { fileUrl } = await response.json()
//   return fileUrl
// }

export async function createProject(formData: FormData): Promise<{ success: boolean, project?: Project, error?: string }> {
  try {

    const user = await getUser()
    if (!user?.userData?.allProjects) {
      throw new Error('User not authenticated or projects not found')
    }

    // 1. Upload the file first
    // const file = formData.get('file') as File
    // const fileUrl = await uploadFileToBackend(file)

    // 2. Create the project payload
    const newProject = {
      id: crypto.randomUUID() as string, // In production, this would come from your DB
      name: formData.get('name') as string,
      description: formData.get('description') as string,
      // industry: formData.get('industry') as string,
      sourceLanguage: formData.get('sourceLanguage') as string,
      destinationLanguage: formData.get('destinationLanguage') as string,
      status: 'Planned',
      priority: 'Normal',
      createdAt: new Date().toISOString(),
    }

    //
    // // 3. Send POST request to create project
    // const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/projects`, {
    //   method: 'POST',
    //   headers: {
    //     'Content-Type': 'application/json',
    //     // Add any auth headers if needed
    //     // 'Authorization': `Bearer ${session.token}`,
    //   },
    //   body: JSON.stringify(projectData),
    // })
    //
    // if (!response.ok) {
    //   throw new Error('Failed to create project')
    // }
    //
    // const newProject = await response.json()

    revalidatePath('/')
    return { success: true, project: newProject }
  } catch (error) {
    console.error('Failed to create project:', error)
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Failed to create project'
    }
  }
} 
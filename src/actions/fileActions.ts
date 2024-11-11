'use server'

export async function detectFileLanguage(file: File) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('/api/detect-language', {
        method: 'POST',
        body: formData,
    });

    if (!response.ok) {
        throw new Error('Failed to detect language');
    }

    const data = await response.json();
    return data.language;
} 
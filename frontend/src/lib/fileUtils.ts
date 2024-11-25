export const MAX_FILE_SIZE = 10 * 1024 * 1024 // 10MB

export const SUPPORTED_FILE_TYPES = {
    'application/pdf': ['.pdf'],
    'application/msword': ['.doc'],
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx']
} as const

export function validateFile(file: File): { valid: boolean; error?: string } {
    // Check file size
    if (file.size > MAX_FILE_SIZE) {
        return {
            valid: false,
            error: `File size must be less than ${formatFileSize(MAX_FILE_SIZE)}`
        }
    }

    // Check file type
    const fileType = file.type
    if (!Object.keys(SUPPORTED_FILE_TYPES).includes(fileType)) {
        return {
            valid: false,
            error: 'File must be .doc, .docx, or .pdf'
        }
    }

    return { valid: true }
}

export function formatFileSize(bytes: number): string {
    const units = ['B', 'KB', 'MB', 'GB']
    let size = bytes
    let unitIndex = 0

    while (size >= 1024 && unitIndex < units.length - 1) {
        size /= 1024
        unitIndex++
    }

    return `${size.toFixed(1)} ${units[unitIndex]}`
} 
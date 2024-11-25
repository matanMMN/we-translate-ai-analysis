'use server'

import {getTextExtractor} from "office-text-extractor";

export async function detectFileLanguage(formData: FormData) {
    const file = formData.get('file') as File
    console.log(file)

    if (!file) {
        throw new Error('No file provided')
    }
    try {
        const extractor = getTextExtractor()
        const buffer = Buffer.from(await file.arrayBuffer())
        const text = await extractor.extractText({input: buffer, type: 'buffer'})
        console.log(text)
        return detectLanguage(text)
    } catch (error) {
        throw new Error('Failed to detect language', error as ErrorOptions)
    }
}

function detectLanguage(text: string) {
    // split into words
    const langs = text.trim().split(/\s+/).map(word => {
        return detect(word)
    })

    // pick the lang with the most occurances
    return (langs || []).reduce((acc: { k: Record<string, number>; max: string | null }, el) => {
        if (!el) return acc
        acc.k[el] = acc.k[el] ? acc.k[el] + 1 : 1
        acc.max = acc.max ? acc.k[acc.max] < acc.k[el] ? el : acc.max : el
        return acc
    }, {k: {}, max: null}).max
}

function detect(text: string) {
    const scores: Record<string, number> = {}

    const regexes = {
        'English': /[\u0000-\u007F]/gi,
        'Chinese': /[\u3000\u3400-\u4DBF\u4E00-\u9FFF]/gi,
        'Hindi': /[\u0900-\u097F]/gi,
        'Arabic': /[\u0621-\u064A\u0660-\u0669]/gi,
        'Bengali': /[\u0995-\u09B9\u09CE\u09DC-\u09DF\u0985-\u0994\u09BE-\u09CC\u09D7\u09BC]/gi,
        'Hebrew': /[\u0590-\u05FF]/gi,
    }

    for (const [lang, regex] of Object.entries(regexes)) {
        // detect occurances of lang in a word
        const matches = text.match(regex) || []
        const score = matches.length / text.length
        if (score) {
            // high percentage, return result
            if (score > 0.85) {
                return lang
            }
            scores[lang] = score
        }
    }

    // not detected
    if (Object.keys(scores).length == 0)
        return null

    // pick lang with highest percentage
    return Object.keys(scores).reduce((a, b) => scores[a] > scores[b] ? a : b)
}

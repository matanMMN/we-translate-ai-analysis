import {MedicalTerm} from "@/components/medicalTerms/TermCard";


interface FetchParams {
    page: number;
    search?: string;
    language: 'hebrew' | 'english';
    limit?: number;
}

// Mock data
const mockTerms: MedicalTerm[] = [
    {
        id: '1',
        hebrewText: 'לב',
        englishText: 'Heart',
        description: 'The vital organ that pumps blood throughout the body',
        createdAt: new Date(),
        updatedAt: new Date(),
    },
    {
        id: '2',
        hebrewText: 'ריאות',
        englishText: 'Lungs',
        description: 'Organs of respiration where gas exchange occurs',
        createdAt: new Date(),
        updatedAt: new Date(),
    },
    {
        id: '3',
        hebrewText: 'כבד',
        englishText: 'Liver',
        description: 'Large organ involved in protein synthesis and detoxification',
        createdAt: new Date(),
        updatedAt: new Date(),
    },
    {
        id: '4',
        hebrewText: 'כליות',
        englishText: 'Kidneys',
        description: 'Organs that filter blood and produce urine',
        createdAt: new Date(),
        updatedAt: new Date(),
    },
    {
        id: '5',
        hebrewText: 'מוח',
        englishText: 'Brain',
        description: 'Central organ of the nervous system',
        createdAt: new Date(),
        updatedAt: new Date(),
    },
    {
        id: '6',
        hebrewText: 'קיבה',
        englishText: 'Stomach',
        description: 'Digestive organ that breaks down food',
        createdAt: new Date(),
        updatedAt: new Date(),
    },
    {
        id: '7',
        hebrewText: 'עצמות',
        englishText: 'Bones',
        description: 'Rigid organs that form the skeleton',
        createdAt: new Date(),
        updatedAt: new Date(),
    },
    {
        id: '8',
        hebrewText: 'שרירים',
        englishText: 'Muscles',
        description: 'Tissues that enable movement',
        createdAt: new Date(),
        updatedAt: new Date(),
    },
    {
        id: '9',
        hebrewText: 'עור',
        englishText: 'Skin',
        description: 'The largest organ of the body',
        createdAt: new Date(),
        updatedAt: new Date(),
    },
];

export async function fetchMedicalTerms({
    page,
    search = '',
    limit = 9,
}: FetchParams) {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 500));

    // Filter terms based on search
    let filteredTerms = mockTerms.filter(term => {
        const searchLower = search.toLowerCase();
        return term.hebrewText.toLowerCase().includes(searchLower) ||
               term.englishText.toLowerCase().includes(searchLower) ||
               term.description.toLowerCase().includes(searchLower);
    });

    // Calculate pagination
    const total = filteredTerms.length;
    const offset = (page - 1) * limit;
    filteredTerms = filteredTerms.slice(offset, offset + limit);

    return {
        terms: filteredTerms,
        total,
    };
}
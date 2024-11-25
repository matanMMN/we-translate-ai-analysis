import { containsRTL } from './textUtils';

export const createSfdtContent = (text: string) => {
    const isRTL = containsRTL(text);
    
    return {
        sections: [{
            sectionFormat: {
                pageWidth: 612,
                pageHeight: 792,
                leftMargin: 72,
                rightMargin: 72,
                topMargin: 72,
                bottomMargin: 72,
                bidi: isRTL
            },
            blocks: text.split('\n')
                .map(paragraph => ({
                    paragraphFormat: {
                        afterSpacing: 6,
                        lineSpacing: 1.15,
                        bidi: isRTL,
                        textAlignment: isRTL ? 'Right' : 'Left',
                        rightIndent: 0,
                        leftIndent: 0
                    },
                    inlines: [{
                        text: paragraph,
                        characterFormat: {
                            fontSize: 11,
                            fontFamily: isRTL ? 'Arial' : 'Calibri',
                            bidi: isRTL
                        }
                    }]
                }))
                .filter(block => block.inlines[0].text.trim() !== '')
        }]
    };
}; 
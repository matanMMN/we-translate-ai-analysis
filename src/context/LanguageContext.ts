
export enum ClientTextMessage{
    TEXT_INPUT_PLACEHOLDER_TEXT = "write_here",
    TRANSLATION_TEXT = "translation",
    TEXT_TEXT = "text",
    SETTINGS_TEXT = "settings_text",
    GENERATE_BUTTON_TEXT = "generate_button",
    TRANSLATE_BUTTON_TEXT = "translate_button",
    REFERENCE_FILE_LABEL_TEXT = "reference_file_label",
    NO_SELECTED_FILE_TEXT = "no_selected_file",
    HEBREW_LANGUAGE_TEXT = "hebrew_lang_text",
    ENGLISH_LANGUAGE_TEXT = "english_text",
    ARABIC_LANGUAGE_TEXT = "arabic_text",
    LANGUAGE_TEXT = "language_text",
    WEBSITE_HEADER_TEXT = "website_header_text",
    SUPPORTED_FILE_TEXT = "support_file_types_text",
    FILE_NOT_FOUND_TEXT = "file_not_found",
    DRAG_AND_DROP_FILE_TEXT = "drag_and_drop",
    BROWSE_FILE_TEXT = "browse_file_text",
    OR_TEXT = "ortext",
    SUCCESS_REFERENCE_UPLOAD_TEXT = "reference_success",
    FAIL_REFERENCE_UPLOAD_TEXT = "reference_failed",
    P_TEXT = "p_text",
    PART_TEXT = "part_Text",
    INVALID_INPUT_TEXT = "invalid_input_text",
    CANCEL_TEXT = "cancel_text",
    WARNING_TEXT = "warning_text",
    ENTER_INPUT_TEXT = "enter_input_text",
    CONTINUE_TEXT = "continue_text",
    MISSING_CREDS_TEXT = "missing_creds_text",
    SUCCESSFUL_COPY = "successful_copy_text",
    TRANSLATION_PART_TEXT = "translation_part_text",
    REFERENCE_FILE_NOT_UPLOAD_TEXT = "reference_file_not_uploaded_text",
    ERROR_TEXT_DOES_NOT_CONTAINS_HEBREW = "no_hebrew",
    INPUT_TOO_SHORT_TEXT = "input_short",
    INPUT_TOO_LONG_TEXT = "input_long",
    INPUT_EMPTY_TEXT = "input_empty"

}

export enum ClientLanguages {
    HEBREW = 'heb',
    ENGLISH = "eng",
    ARABIC = "ara",
};

export const languages = Object.values(ClientLanguages);

export function createLanguageText(textsObject: { [key: string]: string }): { [key: string]: string } {
    const output: { [key: string]: string } = {};
    languages.forEach((lang) => {
        if (textsObject[lang] && textsObject[lang] !== '') {
            output[lang] = textsObject[lang];
        }
    })
    return output;
}


class Language{
    staticTexts = {
        [ClientTextMessage.TEXT_INPUT_PLACEHOLDER_TEXT]: createLanguageText({[ClientLanguages.HEBREW]: "הקלד כאן...", [ClientLanguages.ENGLISH]:"הקלד כאן..."}),
        [ClientTextMessage.TRANSLATION_TEXT]: createLanguageText({[ClientLanguages.HEBREW]: "תרגום", [ClientLanguages.ENGLISH]:"Translation"}),
        [ClientTextMessage.TEXT_TEXT]: createLanguageText({[ClientLanguages.HEBREW]: "טקסט", [ClientLanguages.ENGLISH]:"Text"}),
        [ClientTextMessage.SETTINGS_TEXT]: createLanguageText({[ClientLanguages.HEBREW]: "הגדרות", [ClientLanguages.ENGLISH]:"Settings"}),
        [ClientTextMessage.GENERATE_BUTTON_TEXT]: createLanguageText({[ClientLanguages.HEBREW]: "תרגם הכל", [ClientLanguages.ENGLISH]:"Translate All"}),
        [ClientTextMessage.TRANSLATE_BUTTON_TEXT]: createLanguageText({[ClientLanguages.HEBREW]: "תרגם", [ClientLanguages.ENGLISH]:"Translate"}),
        [ClientTextMessage.REFERENCE_FILE_LABEL_TEXT]: createLanguageText({[ClientLanguages.HEBREW]: ":קובץ ייחוס", [ClientLanguages.ENGLISH]:"Reference File:"}),
        [ClientTextMessage.NO_SELECTED_FILE_TEXT]: createLanguageText({[ClientLanguages.HEBREW]: "קובץ לא נבחר", [ClientLanguages.ENGLISH]:"No file selected"}),
        [ClientTextMessage.HEBREW_LANGUAGE_TEXT]: createLanguageText({[ClientLanguages.HEBREW]: "עברית", [ClientLanguages.ENGLISH]:"Hebrew"}),
        [ClientTextMessage.ENGLISH_LANGUAGE_TEXT]: createLanguageText({[ClientLanguages.HEBREW]: "אנגלית", [ClientLanguages.ENGLISH]:"English"}),
        [ClientTextMessage.ARABIC_LANGUAGE_TEXT]: createLanguageText({[ClientLanguages.HEBREW]: "ערבית", [ClientLanguages.ENGLISH]:"Arabic"}),
        [ClientTextMessage.LANGUAGE_TEXT]: createLanguageText({[ClientLanguages.HEBREW]: "שפה", [ClientLanguages.ENGLISH]:"language"}),
        [ClientTextMessage.WEBSITE_HEADER_TEXT]: createLanguageText({[ClientLanguages.HEBREW]: "תרגום עלוני תרופות", [ClientLanguages.ENGLISH]:"Drug Leaflets Translation"}),
        [ClientTextMessage.SUPPORTED_FILE_TEXT]: createLanguageText({[ClientLanguages.HEBREW]: "DOC, PDF "+ " סוגי קבצים הנתמכים", [ClientLanguages.ENGLISH]:"Supported file types: Docs, PDF"}),
        [ClientTextMessage.FILE_NOT_FOUND_TEXT]: createLanguageText({[ClientLanguages.HEBREW]: "קובץ לא נמצא", [ClientLanguages.ENGLISH]:"File not found"}),
        [ClientTextMessage.DRAG_AND_DROP_FILE_TEXT]: createLanguageText({[ClientLanguages.HEBREW]: "גרור קובץ ושחרר" , [ClientLanguages.ENGLISH]:"Drag And drop your files"}),
        [ClientTextMessage.BROWSE_FILE_TEXT]: createLanguageText({[ClientLanguages.HEBREW]: "בחר קובץ", [ClientLanguages.ENGLISH]:"Browse file"}),
        [ClientTextMessage.OR_TEXT]: createLanguageText({[ClientLanguages.HEBREW]: "או", [ClientLanguages.ENGLISH]:"OR"}),
        [ClientTextMessage.SUCCESS_REFERENCE_UPLOAD_TEXT]: createLanguageText({[ClientLanguages.HEBREW]: "קובץ ייחוס הועלה בהצלחה!", [ClientLanguages.ENGLISH]:"reference file uploaded successfuly!"}),
        [ClientTextMessage.FAIL_REFERENCE_UPLOAD_TEXT]: createLanguageText({[ClientLanguages.HEBREW]: "העלאת קובץ יחוס נכשלה", [ClientLanguages.ENGLISH]:"failed to upload reference file"}),
        [ClientTextMessage.P_TEXT]: createLanguageText({[ClientLanguages.HEBREW]: "פ", [ClientLanguages.ENGLISH]:"P"}),
        [ClientTextMessage.INVALID_INPUT_TEXT]: createLanguageText({[ClientLanguages.HEBREW]: "טקסט שגוי", [ClientLanguages.ENGLISH]:"invalid input"}),
        [ClientTextMessage.PART_TEXT]: createLanguageText({[ClientLanguages.HEBREW]: "חלק", [ClientLanguages.ENGLISH]:"Part"}),
        [ClientTextMessage.CANCEL_TEXT]: createLanguageText({[ClientLanguages.HEBREW]: "ביטול", [ClientLanguages.ENGLISH]:"Cancel"}),
        [ClientTextMessage.WARNING_TEXT]: createLanguageText({[ClientLanguages.HEBREW]: "אזהרה", [ClientLanguages.ENGLISH]:"Warning"}),
        [ClientTextMessage.ENTER_INPUT_TEXT]: createLanguageText({[ClientLanguages.HEBREW]: "אנא הכנס טקסט", [ClientLanguages.ENGLISH]:"please enter text"}),
        [ClientTextMessage.CONTINUE_TEXT]: createLanguageText({[ClientLanguages.HEBREW]: "המשך", [ClientLanguages.ENGLISH]:"Continue"}),
        [ClientTextMessage.MISSING_CREDS_TEXT]: createLanguageText({[ClientLanguages.HEBREW]: "חסר שם משתמש או סיסמא", [ClientLanguages.ENGLISH]:"missing username or password"}),
        [ClientTextMessage.SUCCESSFUL_COPY]: createLanguageText({[ClientLanguages.HEBREW]: "הועתק בהצלחה", [ClientLanguages.ENGLISH]:"successfuly copied"}),
        [ClientTextMessage.TRANSLATION_PART_TEXT]: createLanguageText({[ClientLanguages.HEBREW]: "חלק", [ClientLanguages.ENGLISH]:"Part"}),
        [ClientTextMessage.REFERENCE_FILE_NOT_UPLOAD_TEXT]: createLanguageText({[ClientLanguages.HEBREW]: "?"+"קובץ ייחוס לא הועלה, אתה בטוח שאתה רוצה להמשיך", [ClientLanguages.ENGLISH]:"Reference File Was Not Uploaded, Are You Sure You Want To Continue?"}),
        [ClientTextMessage.ERROR_TEXT_DOES_NOT_CONTAINS_HEBREW]: createLanguageText({[ClientLanguages.HEBREW]: "טקסט אינו מכיל עברית", [ClientLanguages.ENGLISH]:"text does not contains hebrew"}),
        [ClientTextMessage.INPUT_TOO_SHORT_TEXT]: createLanguageText({[ClientLanguages.HEBREW]: "טקסט קצר מידי", [ClientLanguages.ENGLISH]:"text too short"}),
        [ClientTextMessage.INPUT_EMPTY_TEXT]: createLanguageText({[ClientLanguages.HEBREW]: "טקסט ריק", [ClientLanguages.ENGLISH]:"empty text"}),
        [ClientTextMessage.INPUT_TOO_LONG_TEXT]: createLanguageText({[ClientLanguages.HEBREW]: "טקסט ארוך מידי", [ClientLanguages.ENGLISH]:"text too long"}),


    }
}

const language = new Language();

export function getClientStaticLanguageText(lang:ClientLanguages ,text:ClientTextMessage){
    return language.staticTexts[text][lang] || "";
}

export function getServerText(textObject:any,lang:string){
    return textObject[lang] || "";
}

export function isValidLanguage(value:string){
    return Object.values(ClientLanguages).some((lang) => lang === value);
}


export default language;

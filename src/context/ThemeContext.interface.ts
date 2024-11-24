export interface Theme {
    title: string;
    colors: {
        mainColor: string;
        background: string;
        primary: string;
        secondary: string;
        primaryText: string;
        text: string;
        buttonBackground: string;
        buttonText: string;
        error: string;
        success: string;
        warning: string;
        info: string;
    },
    typography: {
        default: {
            fontFamily: string;
            fontSize: string;
        }
    },
    components: {
        dropdown: {
            backgroundColor: string;
            color: string;
        },
        other: {
            backgroundColor: string;
        },
        part: {
            backgroundColor: string;
        },
        button: {
            primary: {
                backgroundColor: string;
                color: string;
                hoverBackground: string;
                hoverColor: string;
            },
            alt_primary: {
                backgroundColor: string;
                color: string;
            },
            secondary: {
                backgroundColor: string;
                color: string;
                hoverBackground: string;
                hoverColor: string;
            },
            alt_secondary: {
                backgroundColor: string;
                color: string;
                hoverBackground: string;
                hoverColor: string;
            },
            alt_secondary_green: {
                backgroundColor: string;
                color: string;
                hoverBackground: string;
                hoverColor: string;
            }
        },
        input: {
            inputText: {
                fontSize: number
            },
            outputText: {
                fontSize: number
            },
            output: {
                backgroundColor: string;

            },
            outputPlaceholder: {
                backgroundColor: string;
            },
            input: {
                fontSize: string
            },
            inputPlaceholder: {
                fontSize: string
            },
            color: string;
            borderColor: string;
            backgroundColor: string;
            placeholderColor: string
        },
    }
}

export interface ThemeContextProps {
    theme: Theme;
    toggleTheme: () => void;
}
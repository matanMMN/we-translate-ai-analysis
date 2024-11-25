import {Theme} from "@/context/ThemeContext.interface";

export const lightTheme: Theme = {
    title: "Default Theme",
    colors: {
        mainColor: "#203F3A",
        background: "#FFFFFF",
        primary: "#0D0630",
        secondary: "#7a99bc",
        primaryText: "#F2F7FA",
        text: "#222222",
        buttonBackground: "#34568b",
        buttonText: "#ffffff",
        error: "#cc3333",
        success: "#6ba833",
        warning: "#ffcc33",
        info: "#6699cc"
    },
    typography: {
        default: {
            fontFamily: "font-family: Arial, sans-serif",
            fontSize: "1rem",
        },
    },
    components: {
        dropdown: {
            backgroundColor: "white",
            color: "black",
        },
        other: {
            backgroundColor: "#13C17C"
        },
        part: {
            backgroundColor: "#E8F9F2"
        },
        button: {
            primary: {
                backgroundColor: "#13C17C",
                color: "",
                hoverBackground: "",
                hoverColor: ""
            },
            alt_primary: {
                backgroundColor: "#02B9F3",
                color: "black",
                // hoverBackground: "",
                // hoverColor: ""
            },
            secondary: {
                backgroundColor: "",
                color: "",
                hoverBackground: "",
                hoverColor: ""
            },
            alt_secondary: {
                backgroundColor: "#E6F8FE",
                color: "#02B9F3",
                hoverBackground: "",
                hoverColor: ""
            },
            alt_secondary_green: {
                backgroundColor: "#E8F9F2",
                color: "#13C17C",
                hoverBackground: "",
                hoverColor: ""
            },
        },
        input: {
            inputText: {
                fontSize: 20,
            },
            outputText: {
                fontSize: 20,
            },
            output: {
                backgroundColor: "#F3F7F9",

            },
            outputPlaceholder: {
                backgroundColor: "#F3F7F9",

            },
            input: {
                fontSize: "1rem"
            },
            inputPlaceholder: {
                fontSize: "1rem"

            },
            backgroundColor: "",
            borderColor: "",
            color: "",
            placeholderColor: ""
        }
    }
}

export const darkTheme: Theme = {} as unknown as never;

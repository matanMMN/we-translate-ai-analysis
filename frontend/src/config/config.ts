import {Config} from "./config.interface";

const config: Config = (() => {

    const env = process.env.NODE_ENV;
    // const isDev = env === "development";
    const isDev = true;
    const serverUrl = isDev ? process.env.REACT_APP_API_URL : "";

    return {
        env,
        serverUrl,
        isDev
    };
})();

export default config;
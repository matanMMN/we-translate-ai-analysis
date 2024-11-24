export interface Config {
    env: "development" | "production" | "test";
    serverUrl: string | undefined;
    isDev: boolean;
}
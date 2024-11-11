// src/api/ApiClient.ts

import axios, {AxiosInstance, AxiosRequestConfig, AxiosResponse, Cancel, CancelTokenSource} from 'axios';
import config from '../config/config';
import {User, user} from "@/lib/userData";


type HTTPMethod = 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';

interface RequestParams {
    [key: string]: string;
}

interface RequestHeaders {
    [key: string]: string;
}

interface Auth {
    accessToken?: string | null
}

class ApiClient {
    private static instance: ApiClient;
    private baseUrl: string | undefined;
    // private languagePreference: string;
    private defaultHeaders: RequestHeaders;
    private axiosInstance: AxiosInstance;
    private cancelTokenSource: CancelTokenSource;
    private defaultTimeout: number

    private constructor() {
        this.defaultTimeout = 10000;
        this.baseUrl = config.serverUrl;
        // this.languagePreference = this.mapLanguage(navigator.language);
        this.defaultHeaders = {
            'Content-Type': 'application/json',
            // 'Accept-Language': this.languagePreference,
            'X-Content-Type-Options': 'nosniff',
            'Referrer-Policy': 'no-referrer-when-downgrade',
        };

        this.cancelTokenSource = axios.CancelToken.source();

        this.axiosInstance = axios.create({
            baseURL: this.baseUrl,
            headers: this.defaultHeaders,
            timeout: this.defaultTimeout, // can be overridden per request
        });

        // Request interceptor to attach Authorization header if needed
        this.axiosInstance.interceptors.request.use(
            (config) => {
                return config;
            },
            (error) => Promise.reject(error)
        );

        // Response interceptor for handling responses globally
        this.axiosInstance.interceptors.response.use(
            (response) => response,
            (error) => {
                if (axios.isCancel(error)) {
                    this.handleRequestCancel(error);
                } else if (error.code === 'ECONNABORTED') {
                    this.handleTimeout(error);
                } else {
                    this.handleApiError(error);
                }
                return Promise.reject(error);
            }
        );

        ApiClient.instance = this;
    }

    handleApiError(error: { response: string; message: string; }) {
        console.error('API Error:', error.response || error.message);
    }

    handleRequestCancel(error: Cancel) {
        console.error('Request canceled:', error.message);
    }

    handleTimeout(error: Cancel) {
        console.error('Request timeout:', error.message);
    }

    public static getInstance(): ApiClient {
        if (!ApiClient.instance) {
            ApiClient.instance = new ApiClient();
        }
        return ApiClient.instance;
    }

    /**
     * Aborts all ongoing requests.
     */
    public abortRequests(): void {
        this.cancelTokenSource.cancel('Operation canceled by the user.');
        this.cancelTokenSource = axios.CancelToken.source();
    }

    /**
     * Aborts requests after a specified time length.
     * @param timeLength Time in milliseconds after which to abort the requests.
     */
    public abortRequestsByTimeLength(timeLength: number): void {
        setTimeout(() => {
            this.abortRequests();
        }, timeLength);
    }

    /**
     * Gets the current language preference.
     */
    // public getLanguagePreference(): string {
    //     return this.languagePreference;
    // }

    /**
     * Maps the browser language to the application's language settings.
     * @param language The browser's language string.
     */
    private mapLanguage(language: string): string {
        return language;
    }

    /**
     * Sets the language preference for the client.
     * @param language The language code to set.
     */
    public setLanguagePreference(language: string): void {
        // this.languagePreference = language;
        this.defaultHeaders['Accept-Language'] = language;
        this.axiosInstance.defaults.headers['Accept-Language'] = language;
    }

    /**
     * Generic request method using axios.
     * @param path The API endpoint path.
     * @param method The HTTP method.
     * @param data The request payload.
     * @param headers Additional headers.
     * @param params Query parameters.
     * @param auth
     * @param timeout Request timeout in milliseconds.
     */
    private async _request<T>(
        path: string,
        method: HTTPMethod,
        data: { accessToken: string } | FormData | null = null,
        headers: RequestHeaders | null = null,
        params: RequestParams | null | FormData = null,
        auth: Auth | null = null,
        timeout: number = this.defaultTimeout
    ): Promise<AxiosResponse<T>> {
        const config: AxiosRequestConfig = {
            url: path,
            method: method,
            headers: headers || this.defaultHeaders,
            params: params || {},
            data: data,
            cancelToken: this.cancelTokenSource.token,
            timeout: timeout,
        };

        if (auth) {
            if (auth.accessToken != undefined) {
                config.headers = {
                    ...config.headers,
                    Authorization: auth.accessToken && `Bearer ${auth.accessToken}`,
                };
            }

        }

        try {
            const response = await this.axiosInstance.request<T>(config);
            return response;
        } catch (error) {
            if (axios.isCancel(error)) {
                throw new Error('Request was canceled');
            } else if ((error as { code: string }).code === 'ECONNABORTED') {
                this.abortRequests();
                throw new Error('Request timed out');
            } else {
                if (config.method !== 'GET' && config.method !== 'DELETE') {
                    console.error('Error in request:', (error as { response: string }).response || (error as {
                        message: string
                    }).message);
                }
                throw error;
            }
        }
    }


    private formatFilters(filters: Record<string, undefined> | null) {
        const formattedFilters: Record<string, undefined> = {
            ...filters,
        };
        return formattedFilters;
    }

    private async _Many(
        path: string,
        method: HTTPMethod,
        data?: { accessToken: string } | null,
        headers?: RequestHeaders | null,
        params?: RequestParams | null,
        auth?: Auth | null,
        timeout?: number,
        page: number | null = null,
        pageSize: number | null = null,
        filters: Record<string, undefined> | null = null,
        searchQuery: string | null = null,
        sortBy: string | null = null,
        sortOrder: number | null = null,
    ): Promise<AxiosResponse> {
        const formattedFilters: Record<string, undefined> = this.formatFilters(filters);
        const allParams = {
            page,
            page_size: pageSize,
            search_query: searchQuery,
            sort_by: sortBy,
            sort_order: sortOrder,
            ...formattedFilters,
            ...params,
        } as unknown as FormData;
        return this._request(path, method, data, headers, allParams, auth, timeout);
    }

    public async ping(): Promise<AxiosResponse> {
        return this._request('/api/ping', 'GET');
    }


    public async register(): Promise<AxiosResponse> {
        return this._request('/auth/register', 'GET');
    }

    public async login(email: string, password: string): Promise<User> {
        const body = {email, password};
        console.log(body)
        // return this._request<any>('/login', 'POST', body);
        return user as unknown as User
    }


    public async uploadFile(auth: Auth, file: File): Promise<AxiosResponse> {
        const formData = new FormData();
        formData.append('file', file);
        const headers: RequestHeaders = {
            'Content-Type': 'multipart/form-data',
        };
        return this._request('/files/upload', 'POST', formData, headers, null, auth);
    }

    public async downloadFile(auth: Auth, fileId: string): Promise<AxiosResponse<Blob>> {
        return this._request<Blob>(`/files/download/${fileId}`, 'GET', null, {responseType: 'blob'} as RequestHeaders, null, auth);
    }

    public async deleteFile(auth: Auth, fileId: string): Promise<AxiosResponse> {
        return this._request(`/files/${fileId}`, 'DELETE', null, null, null, auth);
    }

    public async getFileById(auth: Auth, fileId: string): Promise<AxiosResponse> {
        return this._request(`/files/id/${fileId}`, 'GET', null, null, null, auth);
    }

    public async getFileByTitle(auth: Auth, fileTitle: string): Promise<AxiosResponse> {
        return this._request(`/files/title/${fileTitle}`, 'GET', null, null, null, auth);
    }
}


const apiClient = ApiClient.getInstance();
export default apiClient;






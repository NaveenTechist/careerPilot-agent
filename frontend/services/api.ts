import axios from "axios";

export const api = axios.create({
    baseURL: "http://localhost:8000",
    timeout: 30000,
});

api.interceptors.response.use(

    response => response,

    error => {

        const message =
            error.response?.data?.detail ??
            "Unexpected server error.";

        return Promise.reject(
            new Error(message)
        );
    }

);
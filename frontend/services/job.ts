import { api } from "./api";

export async function analyzeJob(
    url: string
) {

    const response =
        await api.post(
            "/job/",
            {
                url,
            }
        );

    return response.data;
}
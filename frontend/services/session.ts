import { api } from "./api";
export async function getSession() {
    const response =
        await api.get(
            "/session/"
        );
    return response.data;
}
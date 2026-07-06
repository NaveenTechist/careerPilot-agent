import { api } from "./api";

export async function matchResume() {

    const response =
        await api.post(
            "/match/"
        );

    return response.data;
}

export async function proceedMatch(
    id: string
) {

    return api.post(
        `/match/${id}/proceed`
    );
}

export async function cancelMatch(
    id: string
) {

    return api.post(
        `/match/${id}/cancel`
    );
}
import { api } from "./api";

export async function uploadResume(file: File) {
    const form = new FormData();
    form.append(
        "file",
        file
    );
    const response =
        await api.post(
            "/resume/",
            form,
            {
                headers: {
                    "Content-Type":
                        "multipart/form-data",
                },
            }
        );
    return response.data;
}
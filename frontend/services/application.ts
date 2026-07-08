import { api } from "./api";

export async function createApplication(resume: File, jobUrl: string) {
    const form = new FormData();
    form.append("resume", resume);
    form.append("job_url", jobUrl);

    const response = await api.post("/application", form, {
        headers: {
            "Content-Type": "multipart/form-data",
        },
    });
    return response.data;
}

export async function getApplications() {
    const response = await api.get("/applications");
    return response.data;
}

export async function getApplicationDetails(id: string) {
    const response = await api.get(`/applications/${id}`);
    return response.data;
}

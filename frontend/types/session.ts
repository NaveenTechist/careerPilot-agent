export interface Session {
    status: string;
    resume: {
        uploaded: boolean;
        profile: any;
    };
    job: {
        uploaded: boolean;
        profile: any;
    };
}
export interface MatchResult {
    id: string;
    score: number;
    overall_level: string;
    matched_skills: string[];
    missing_skills: string[];
    strengths: string[];
    weaknesses: string[];
    recommendation: string;
    should_apply: boolean;
    result: string;
    match_id: string;
}
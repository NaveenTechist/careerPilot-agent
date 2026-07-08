class MatchResponse(BaseModel):

    match_id: UUID
    status: MatchStatus
    result: MatchResult
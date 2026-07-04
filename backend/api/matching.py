"""
Matching API.
"""

import time
import uuid

from fastapi import APIRouter, Depends

from agents.matching_agent import MatchingAgent
from services.matching_parser_service import (
    MatchingParserService,
)

from core.logger import app_logger

router = APIRouter(
    prefix="/match",
    tags=["Matching"],
)


def get_matching_agent():

    parser = MatchingParserService()

    return MatchingAgent(
        parser,
    )


@router.post("/")
def match_resume(
    matching_agent: MatchingAgent = Depends(
        get_matching_agent
    ),
):

    request_id = str(uuid.uuid4())

    logger = app_logger.bind(
        request_id=request_id
    )

    start = time.perf_counter()

    logger.info(
        "Matching request received."
    )

    try:

        result = matching_agent.process()

        logger.success(
            "Matching completed."
        )

        return result

    except Exception:

        logger.exception(
            "Matching failed."
        )

        raise

    finally:

        elapsed = (
            time.perf_counter()
            - start
        ) * 1000

        logger.info(
            f"Completed in {elapsed:.2f} ms"
        )
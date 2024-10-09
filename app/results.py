import datetime
import json
import os
from typing import Dict

from fastapi import APIRouter, Response, status, HTTPException, Depends
from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import BenchmarkResult

router = APIRouter()

test_database_file = "test_database.json"


def try_load_test_data(db: Session) -> None:
    debug_mode = os.getenv("SUPERBENCHMARK_DEBUG", "False").lower() in ["true", "t", "1"]

    if not debug_mode:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="The feature is not live yet")

    with open(test_database_file, 'r') as fixture_file:
        fixture_data = json.load(fixture_file)['benchmarking_results']

        for benchmark_data in fixture_data:
            timestamp = datetime.datetime.strptime(benchmark_data['timestamp'], '%Y-%m-%dT%H:%M:%S')

            record = BenchmarkResult(
                request_id=benchmark_data['request_id'],
                prompt_text=benchmark_data['prompt_text'],
                generated_text=benchmark_data['generated_text'],
                token_count=benchmark_data['token_count'],
                time_to_first_token=benchmark_data['time_to_first_token'],
                time_per_output_token=benchmark_data['time_per_output_token'],
                total_generation_time=benchmark_data['total_generation_time'],
                timestamp=timestamp,
            )

            db.add(record)

        db.commit()


@router.get("/", response_model=None)
async def get_average(db: Session = Depends(get_db)) -> Dict[str, float]:
    try_load_test_data(db)

    averages = db.query(
        func.avg(BenchmarkResult.token_count).label("average_token_count"),
        func.avg(BenchmarkResult.time_to_first_token).label("average_time_to_first_token"),
        func.avg(BenchmarkResult.time_per_output_token).label("average_time_per_output_token"),
        func.avg(BenchmarkResult.total_generation_time).label("average_total_generation_time")
    ).one()

    averages_dict = {
        "average_token_count": averages[0],
        "average_time_to_first_token": averages[1],
        "average_time_per_output_token": averages[2],
        "average_total_generation_time": averages[3],
    }

    return averages_dict


@router.get("/{start_time}/{end_time}", response_model=None)
async def get_average_range(
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        db: Session = Depends(get_db),
) -> Dict[str, float] | Response:
    try_load_test_data(db)

    benchmarks_in_range = db.query(BenchmarkResult).filter(
        and_(
            BenchmarkResult.timestamp >= start_time,
            BenchmarkResult.timestamp <= end_time
        )
    )

    if benchmarks_in_range.count() == 0:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    averages = benchmarks_in_range.with_entities(
        func.avg(BenchmarkResult.token_count).label("average_token_count"),
        func.avg(BenchmarkResult.time_to_first_token).label("average_time_to_first_token"),
        func.avg(BenchmarkResult.time_per_output_token).label("average_time_per_output_token"),
        func.avg(BenchmarkResult.total_generation_time).label("average_total_generation_time")
    ).one()

    averages_dict = {
        "average_token_count": averages[0],
        "average_time_to_first_token": averages[1],
        "average_time_per_output_token": averages[2],
        "average_total_generation_time": averages[3],
    }

    return averages_dict

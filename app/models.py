from sqlalchemy import Column, Integer, String, DateTime

from app.database import Base


class BenchmarkResult(Base):  # type: ignore
    __tablename__ = "benchmark_results"

    id = Column(Integer, primary_key=True)
    request_id = Column(String, index=True)
    prompt_text = Column(String)
    generated_text = Column(String)
    token_count = Column(Integer)
    time_to_first_token = Column(Integer)
    time_per_output_token = Column(Integer)
    total_generation_time = Column(Integer)
    timestamp = Column(DateTime)

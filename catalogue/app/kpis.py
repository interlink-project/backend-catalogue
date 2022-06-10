import asyncio
import logging
from app.models import *
from app.general.db.session import SessionLocal
from app.messages import set_logging_disabled
from sqlalchemy.orm import Session
from sqlalchemy.dialects import postgresql

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# https://drive.google.com/u/2/open?id=1VBpL3sIcYRdXbHLmfIs0aYiWYaerWVCH

show_queries = False

def divide(x, y):
    if y == 0:
        print(f"Y ({y}) should be greater than 0")
        return 0
    return x / y

def get_raw_query(q):
    if show_queries:
        print(str(q.statement.compile(dialect=postgresql.dialect()))) 

async def init():
    data = {"interlinkers": {}}

    db: Session = SessionLocal()
    set_logging_disabled(True)

    # Interlinker count
    interlinkers_count_query = db.query(
            Interlinker.id
        )
    interlinkers_count = interlinkers_count_query.count()
    
    get_raw_query(interlinkers_count_query)
    data["interlinkers"]["count"] = interlinkers_count

    # Knowledge count
    interlinkers_count_query = db.query(
            KnowledgeInterlinker.id
        )
    interlinkers_count = interlinkers_count_query.count()
    
    get_raw_query(interlinkers_count_query)
    data["interlinkers"]["knowledge"] = interlinkers_count

    # External Knowledge count
    interlinkers_count_query = db.query(
            ExternalKnowledgeInterlinker.id
        )
    interlinkers_count = interlinkers_count_query.count()
    
    get_raw_query(interlinkers_count_query)
    data["interlinkers"]["externalknowledge"] = interlinkers_count

    # Software count
    interlinkers_count_query = db.query(
            SoftwareInterlinker.id
        )
    interlinkers_count = interlinkers_count_query.count()
    
    get_raw_query(interlinkers_count_query)
    data["interlinkers"]["software"] = interlinkers_count

    # Software count
    interlinkers_count_query = db.query(
            ExternalSoftwareInterlinker.id
        )
    interlinkers_count = interlinkers_count_query.count()
    
    get_raw_query(interlinkers_count_query)
    data["interlinkers"]["externalsoftware"] = interlinkers_count

    db.close()
    return data

if __name__ == "__main__":
    logger.info("Creating initial data")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init())
    logger.info("Initial data created")
    

import sys

# Add the parent directory to Python's path
sys.path.insert(0, '/Users/arthurgao/Code/python/domain-scanner')
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env", override=True)

from uuid import UUID
from mcp.server.fastmcp import FastMCP
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user_scan_result import UserScanResult

# Initialize FastMCP server
mcp = FastMCP("scan-report")

@mcp.tool()
async def get_scan_result(scan_result_id: str) -> str:
    """
    Get the result of a specific user scan by scan_result_id.

    Args:
        scan_result_id: The UUID of the scan result.
    Returns:
        A plain text description of the scan result, or a message if not found.
    """
    db: Session = SessionLocal()
    try:
        scan = db.query(UserScanResult).filter_by(id=UUID(scan_result_id)).first()
        if not scan:
            return "Scan result not found."
        print(scan.id)
        return f"""
            Scan Result ID: {scan.id}
            Scan ID: {scan.scan_id}
            Status: {scan.status.name}
            Started At: {scan.started_at}
            Completed At: {scan.completed_at}
            Result:
            {scan.result}
        """
    finally:
        db.close()

if __name__ == "__main__":
    mcp.run(transport='stdio')
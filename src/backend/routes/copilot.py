"""
Copilot RAG operational report generation endpoints.
"""

from fastapi import APIRouter, HTTPException
from src.backend.models.copilot_models import (
    CopilotReportRequest,
    CopilotReportResponse,
    SourceProvenance
)
from src.rag.copilot import get_copilot

router = APIRouter(prefix="/copilot", tags=["copilot"])


@router.post("/report", response_model=CopilotReportResponse)
async def generate_operational_report(request: CopilotReportRequest):
    """
    Generate an operational briefing report using RAG-based analysis.
    
    This endpoint:
    1. Accepts a risk analysis payload
    2. Retrieves relevant context from the knowledge base
    3. Loads runtime data from processed files
    4. Generates a comprehensive operational briefing
    
    The report includes:
    - Executive summary
    - Evidence summary
    - Recommended actions based on risk level
    - Source provenance for transparency
    - Known limitations and uncertainties
    
    Args:
        request: CopilotReportRequest containing risk analysis data
        
    Returns:
        CopilotReportResponse with operational briefing
        
    Raises:
        HTTPException: If report generation fails
    """
    try:
        # Get copilot instance
        copilot = get_copilot()
        
        # Generate report
        report_data = copilot.generate_report(request.risk_analysis)
        
        # Convert to response model
        response = CopilotReportResponse(
            title=report_data['title'],
            area_of_interest=report_data['area_of_interest'],
            risk_level=report_data['risk_level'],
            risk_score=report_data['risk_score'],
            executive_summary=report_data['executive_summary'],
            evidence_summary=report_data['evidence_summary'],
            source_provenance=SourceProvenance(**report_data['source_provenance']),
            recommended_actions=report_data['recommended_actions'],
            limitations=report_data['limitations'],
            generated_at=report_data['generated_at']
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate operational report: {str(e)}"
        )

# Made with Bob

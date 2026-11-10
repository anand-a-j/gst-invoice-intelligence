from fastapi import APIRouter, Depends, HTTPException, UploadFile,File 
from pydantic import BaseModel, Field

from app.core.config import Settings, get_settings
from app.models.invoice import ExtractionResponse
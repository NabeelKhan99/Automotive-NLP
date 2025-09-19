"""
Automotive NLP
==============

A toolkit for analyzing customer automotive feedback:
- Stores and manages feedback data.
- Runs NLP preprocessing and sentiment analysis.
- Clusters complaints to detect recurring issues.
- Suggests dynamic pricing based on demand.

This package powers both the CLI tool and optional API.
"""

__version__ = "0.1.0"

# Expose key modules at the top level
from . import db
#from . import nlp
from . import services

# Shortcut imports for common usage
from .services.analysis_service import analyze_feedback
from .services.feedback_service import save_feedback

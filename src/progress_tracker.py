"""
Progress Tracking System
Enhanced progress tracking with stage indicators, time estimates, and NIM usage tracking
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from enum import Enum
import time


class Stage(Enum):
    """Research synthesis stages"""
    INITIALIZING = "initializing"
    SEARCHING = "searching"
    ANALYZING = "analyzing"
    SYNTHESIZING = "synthesizing"
    REFINING = "refining"
    COMPLETE = "complete"


class ProgressTracker:
    """
    Tracks progress through research synthesis workflow
    Provides time estimates and stage information
    """
    
    def __init__(self):
        self.start_time: Optional[datetime] = None
        self.current_stage: Stage = Stage.INITIALIZING
        self.stage_start_times: Dict[Stage, datetime] = {}
        self.stage_durations: Dict[Stage, float] = {}
        self.papers_found: int = 0
        self.papers_analyzed: int = 0
        self.papers_total: int = 0
        self.current_nim: Optional[str] = None
        self.stage_progress: float = 0.0  # 0.0 to 1.0 for current stage
        self.history: List[Dict] = []
        
    def start(self):
        """Mark synthesis start"""
        self.start_time = datetime.now()
        self.current_stage = Stage.INITIALIZING
        self.stage_start_times[Stage.INITIALIZING] = self.start_time
        
    def set_stage(self, stage: Stage, nim_used: Optional[str] = None):
        """Transition to a new stage"""
        if self.current_stage != stage:
            # Record duration of previous stage
            if self.current_stage in self.stage_start_times:
                duration = (datetime.now() - self.stage_start_times[self.current_stage]).total_seconds()
                self.stage_durations[self.current_stage] = duration
            
            # Update to new stage
            self.current_stage = stage
            self.stage_start_times[stage] = datetime.now()
            self.stage_progress = 0.0
            self.current_nim = nim_used
            
            # Log stage change
            self.history.append({
                "timestamp": datetime.now().isoformat(),
                "stage": stage.value,
                "nim_used": nim_used,
                "papers_found": self.papers_found,
                "papers_analyzed": self.papers_analyzed
            })
    
    def update_stage_progress(self, progress: float):
        """Update progress within current stage (0.0 to 1.0)"""
        self.stage_progress = max(0.0, min(1.0, progress))
    
    def set_papers_total(self, count: int):
        """Set total number of papers to analyze"""
        self.papers_total = count
    
    def set_papers_found(self, count: int):
        """Update number of papers found"""
        self.papers_found = count
        if self.current_stage == Stage.SEARCHING:
            if self.papers_total > 0:
                self.stage_progress = min(1.0, self.papers_found / self.papers_total)
            else:
                # Estimate: search is typically quick
                self.stage_progress = min(1.0, self.papers_found / 20.0)
    
    def set_papers_analyzed(self, count: int):
        """Update number of papers analyzed"""
        self.papers_analyzed = count
        if self.current_stage == Stage.ANALYZING:
            if self.papers_total > 0:
                self.stage_progress = min(1.0, self.papers_analyzed / self.papers_total)
    
    def get_overall_progress(self) -> float:
        """Get overall progress (0.0 to 1.0)"""
        if self.current_stage == Stage.COMPLETE:
            return 1.0
        
        stage_weights = {
            Stage.INITIALIZING: 0.05,
            Stage.SEARCHING: 0.20,
            Stage.ANALYZING: 0.35,
            Stage.SYNTHESIZING: 0.25,
            Stage.REFINING: 0.15
        }
        
        # Calculate progress based on completed stages
        total_progress = 0.0
        for stage in Stage:
            if stage == Stage.COMPLETE:
                break
            if stage in self.stage_durations:  # Stage completed
                total_progress += stage_weights.get(stage, 0.0)
            elif stage == self.current_stage:  # Current stage
                weight = stage_weights.get(stage, 0.0)
                total_progress += weight * self.stage_progress
                break
        
        return min(1.0, total_progress)
    
    def get_time_elapsed(self) -> float:
        """Get total time elapsed in seconds"""
        if not self.start_time:
            return 0.0
        return (datetime.now() - self.start_time).total_seconds()
    
    def estimate_time_remaining(self) -> Optional[float]:
        """Estimate time remaining based on current stage and progress"""
        if self.current_stage == Stage.COMPLETE:
            return 0.0
        
        elapsed = self.get_time_elapsed()
        if elapsed == 0:
            return None
        
        # Estimate based on typical durations
        # Adjust based on actual progress
        overall_progress = self.get_overall_progress()
        
        if overall_progress > 0:
            # Linear extrapolation
            estimated_total = elapsed / overall_progress
            remaining = estimated_total - elapsed
            
            # Cap estimates to reasonable bounds
            if remaining < 0:
                remaining = 0
            if remaining > 600:  # 10 minutes max
                remaining = 600
            
            return remaining
        
        return None
    
    def get_stage_info(self) -> Dict:
        """Get current stage information"""
        time_remaining = self.estimate_time_remaining()
        
        return {
            "current_stage": self.current_stage.value,
            "stage_progress": self.stage_progress,
            "overall_progress": self.get_overall_progress(),
            "time_elapsed": self.get_time_elapsed(),
            "time_remaining": time_remaining,
            "papers_found": self.papers_found,
            "papers_analyzed": self.papers_analyzed,
            "papers_total": self.papers_total,
            "nim_used": self.current_nim,
            "is_complete": self.current_stage == Stage.COMPLETE
        }
    
    def complete(self):
        """Mark synthesis as complete"""
        self.set_stage(Stage.COMPLETE)
        if self.current_stage in self.stage_start_times:
            duration = (datetime.now() - self.stage_start_times[self.current_stage]).total_seconds()
            self.stage_durations[self.current_stage] = duration


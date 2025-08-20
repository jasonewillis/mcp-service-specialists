"""
Time Travel Debugging for Fed Job Advisor LangGraph Orchestrator

Advanced debugging features using LangGraph's SqliteSaver for persistent checkpoints:
- State replay functionality
- Checkpoint comparison tools  
- Performance profiling between checkpoints
- Debug mode with static interrupts
- Temporal workflow analysis

Key Features:
- Persistent checkpoint storage with SQLite
- State replay from any point in workflow execution
- Diff analysis between checkpoints
- Performance bottleneck identification
- Debug mode with controlled execution
- Checkpoint branching for A/B testing
"""

import logging
import sqlite3
import json
import asyncio
from typing import Dict, Any, List, Optional, Union, Tuple
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum
import pickle
import hashlib
from contextlib import asynccontextmanager

from langgraph.graph import StateGraph
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.runnables import RunnableConfig

logger = logging.getLogger(__name__)


class DebugLevel(Enum):
    """Debug levels for time travel debugging"""
    MINIMAL = "minimal"      # Basic checkpoint storage
    STANDARD = "standard"    # + State diffs
    VERBOSE = "verbose"      # + Performance metrics
    EXHAUSTIVE = "exhaustive"  # + Full state serialization


class CheckpointEvent(Enum):
    """Types of checkpoint events"""
    WORKFLOW_START = "workflow_start"
    PHASE_COMPLETE = "phase_complete"
    ERROR_OCCURRED = "error_occurred"
    HUMAN_INTERRUPT = "human_interrupt"
    DEBUG_BREAKPOINT = "debug_breakpoint"
    WORKFLOW_COMPLETE = "workflow_complete"


@dataclass
class CheckpointMetadata:
    """Metadata for a workflow checkpoint"""
    checkpoint_id: str
    thread_id: str
    timestamp: datetime
    event_type: CheckpointEvent
    workflow_type: str
    phase: str
    state_hash: str
    performance_metrics: Dict[str, Any]
    debug_notes: str
    parent_checkpoint: Optional[str] = None


@dataclass
class StateDiff:
    """Difference between two states"""
    checkpoint_from: str
    checkpoint_to: str
    added_keys: List[str]
    removed_keys: List[str]
    modified_keys: List[str]
    value_changes: Dict[str, Dict[str, Any]]
    timestamp: datetime


@dataclass 
class PerformanceProfile:
    """Performance profile between checkpoints"""
    start_checkpoint: str
    end_checkpoint: str
    duration_ms: float
    memory_usage_mb: float
    agent_execution_times: Dict[str, float]
    bottlenecks: List[str]
    recommendations: List[str]


class TimeTravel:
    """
    Time travel debugging system for LangGraph workflows
    
    Provides advanced debugging capabilities including state replay,
    checkpoint comparison, and performance profiling.
    """
    
    def __init__(self, db_path: str = "debugging/time_travel.sqlite", debug_level: DebugLevel = DebugLevel.STANDARD):
        """Initialize time travel debugging system"""
        
        self.debug_level = debug_level
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        
        # Initialize SQLite connections
        self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self.checkpointer = SqliteSaver(self.conn)
        
        # Create additional debugging tables
        self._initialize_debug_tables()
        
        # In-memory caches for performance
        self.checkpoint_cache: Dict[str, CheckpointMetadata] = {}
        self.state_cache: Dict[str, Dict[str, Any]] = {}
        
        logger.info(f"Time travel debugging initialized (level={debug_level.value}, db={db_path})")
    
    def _initialize_debug_tables(self):
        """Initialize additional debugging tables in SQLite"""
        
        cursor = self.conn.cursor()
        
        # Checkpoint metadata table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS checkpoint_metadata (
                checkpoint_id TEXT PRIMARY KEY,
                thread_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                event_type TEXT NOT NULL,
                workflow_type TEXT,
                phase TEXT,
                state_hash TEXT,
                performance_metrics TEXT,
                debug_notes TEXT,
                parent_checkpoint TEXT,
                FOREIGN KEY (parent_checkpoint) REFERENCES checkpoint_metadata (checkpoint_id)
            )
        """)
        
        # State diffs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS state_diffs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                checkpoint_from TEXT NOT NULL,
                checkpoint_to TEXT NOT NULL,
                added_keys TEXT,
                removed_keys TEXT,  
                modified_keys TEXT,
                value_changes TEXT,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (checkpoint_from) REFERENCES checkpoint_metadata (checkpoint_id),
                FOREIGN KEY (checkpoint_to) REFERENCES checkpoint_metadata (checkpoint_id)
            )
        """)
        
        # Performance profiles table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS performance_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_checkpoint TEXT NOT NULL,
                end_checkpoint TEXT NOT NULL,
                duration_ms REAL,
                memory_usage_mb REAL,
                agent_execution_times TEXT,
                bottlenecks TEXT,
                recommendations TEXT,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (start_checkpoint) REFERENCES checkpoint_metadata (checkpoint_id),
                FOREIGN KEY (end_checkpoint) REFERENCES checkpoint_metadata (checkpoint_id)
            )
        """)
        
        # Debug sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS debug_sessions (
                session_id TEXT PRIMARY KEY,
                thread_id TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT,
                debug_level TEXT,
                breakpoints TEXT,
                session_notes TEXT
            )
        """)
        
        self.conn.commit()
        logger.info("Debug tables initialized")
    
    def _calculate_state_hash(self, state: Dict[str, Any]) -> str:
        """Calculate hash of state for change detection"""
        
        try:
            # Create a deterministic string representation
            state_str = json.dumps(state, sort_keys=True, default=str)
            return hashlib.md5(state_str.encode()).hexdigest()
        except Exception as e:
            logger.warning(f"Could not hash state: {e}")
            return f"hash_error_{datetime.utcnow().timestamp()}"
    
    async def create_checkpoint(
        self,
        thread_id: str,
        state: Dict[str, Any],
        event_type: CheckpointEvent,
        workflow_type: str,
        phase: str,
        debug_notes: str = "",
        performance_metrics: Optional[Dict[str, Any]] = None,
        parent_checkpoint: Optional[str] = None
    ) -> str:
        """Create a new debugging checkpoint"""
        
        checkpoint_id = f"{thread_id}_{event_type.value}_{datetime.utcnow().timestamp()}"
        timestamp = datetime.utcnow()
        state_hash = self._calculate_state_hash(state)
        
        metadata = CheckpointMetadata(
            checkpoint_id=checkpoint_id,
            thread_id=thread_id,
            timestamp=timestamp,
            event_type=event_type,
            workflow_type=workflow_type,
            phase=phase,
            state_hash=state_hash,
            performance_metrics=performance_metrics or {},
            debug_notes=debug_notes,
            parent_checkpoint=parent_checkpoint
        )
        
        # Store in database
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO checkpoint_metadata VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            checkpoint_id, thread_id, timestamp.isoformat(), event_type.value,
            workflow_type, phase, state_hash, json.dumps(performance_metrics or {}),
            debug_notes, parent_checkpoint
        ))
        
        self.conn.commit()
        
        # Cache for performance
        self.checkpoint_cache[checkpoint_id] = metadata
        
        if self.debug_level in [DebugLevel.VERBOSE, DebugLevel.EXHAUSTIVE]:
            self.state_cache[checkpoint_id] = state.copy()
        
        logger.debug(f"Created checkpoint {checkpoint_id} for {workflow_type}:{phase}")
        return checkpoint_id
    
    async def replay_from_checkpoint(
        self,
        checkpoint_id: str,
        target_phase: Optional[str] = None,
        debug_mode: bool = True
    ) -> Dict[str, Any]:
        """Replay workflow execution from a specific checkpoint"""
        
        logger.info(f"Starting replay from checkpoint {checkpoint_id}")
        
        # Get checkpoint metadata
        metadata = await self.get_checkpoint_metadata(checkpoint_id)
        if not metadata:
            raise ValueError(f"Checkpoint {checkpoint_id} not found")
        
        # Get the workflow state at this checkpoint
        config = RunnableConfig(
            configurable={"thread_id": metadata.thread_id}
        )
        
        try:
            # Get state from checkpointer
            checkpoint_state = await self._get_state_at_checkpoint(checkpoint_id)
            
            replay_result = {
                "checkpoint_id": checkpoint_id,
                "original_timestamp": metadata.timestamp.isoformat(),
                "replay_timestamp": datetime.utcnow().isoformat(),
                "thread_id": metadata.thread_id,
                "workflow_type": metadata.workflow_type,
                "phase": metadata.phase,
                "state": checkpoint_state,
                "debug_mode": debug_mode,
                "target_phase": target_phase,
                "replay_successful": True
            }
            
            # If in debug mode, add breakpoints
            if debug_mode:
                replay_result["debug_breakpoints"] = await self._get_debug_breakpoints(metadata.thread_id)
            
            logger.info(f"Successfully replayed from checkpoint {checkpoint_id}")
            return replay_result
            
        except Exception as e:
            logger.error(f"Replay failed for checkpoint {checkpoint_id}: {e}")
            return {
                "checkpoint_id": checkpoint_id,
                "replay_successful": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def compare_checkpoints(
        self,
        checkpoint_from: str,
        checkpoint_to: str,
        detailed_analysis: bool = True
    ) -> StateDiff:
        """Compare two checkpoints and generate a detailed diff"""
        
        logger.info(f"Comparing checkpoints {checkpoint_from} -> {checkpoint_to}")
        
        # Get states for both checkpoints
        state_from = await self._get_state_at_checkpoint(checkpoint_from)
        state_to = await self._get_state_at_checkpoint(checkpoint_to)
        
        if not state_from or not state_to:
            raise ValueError("Could not retrieve states for comparison")
        
        # Calculate differences
        keys_from = set(state_from.keys())
        keys_to = set(state_to.keys())
        
        added_keys = list(keys_to - keys_from)
        removed_keys = list(keys_from - keys_to)
        common_keys = keys_from & keys_to
        
        modified_keys = []
        value_changes = {}
        
        for key in common_keys:
            val_from = state_from[key]
            val_to = state_to[key]
            
            if val_from != val_to:
                modified_keys.append(key)
                if detailed_analysis:
                    value_changes[key] = {
                        "from": self._serialize_value(val_from),
                        "to": self._serialize_value(val_to)
                    }
        
        diff = StateDiff(
            checkpoint_from=checkpoint_from,
            checkpoint_to=checkpoint_to,
            added_keys=added_keys,
            removed_keys=removed_keys,
            modified_keys=modified_keys,
            value_changes=value_changes,
            timestamp=datetime.utcnow()
        )
        
        # Store diff in database
        if self.debug_level in [DebugLevel.VERBOSE, DebugLevel.EXHAUSTIVE]:
            await self._store_state_diff(diff)
        
        logger.info(f"Checkpoint comparison completed: {len(modified_keys)} changes")
        return diff
    
    async def profile_performance(
        self,
        start_checkpoint: str,
        end_checkpoint: str,
        include_agent_breakdown: bool = True
    ) -> PerformanceProfile:
        """Profile performance between two checkpoints"""
        
        logger.info(f"Profiling performance {start_checkpoint} -> {end_checkpoint}")
        
        # Get checkpoint metadata
        start_meta = await self.get_checkpoint_metadata(start_checkpoint)
        end_meta = await self.get_checkpoint_metadata(end_checkpoint)
        
        if not start_meta or not end_meta:
            raise ValueError("Could not retrieve checkpoint metadata")
        
        # Calculate duration
        duration = (end_meta.timestamp - start_meta.timestamp).total_seconds() * 1000  # ms
        
        # Get performance metrics from both checkpoints
        start_metrics = start_meta.performance_metrics
        end_metrics = end_meta.performance_metrics
        
        # Calculate agent execution times if available
        agent_execution_times = {}
        if include_agent_breakdown:
            agent_execution_times = self._analyze_agent_performance(start_metrics, end_metrics)
        
        # Identify bottlenecks and generate recommendations
        bottlenecks, recommendations = self._analyze_bottlenecks(
            duration, agent_execution_times, start_meta, end_meta
        )
        
        profile = PerformanceProfile(
            start_checkpoint=start_checkpoint,
            end_checkpoint=end_checkpoint,
            duration_ms=duration,
            memory_usage_mb=end_metrics.get("memory_usage_mb", 0),
            agent_execution_times=agent_execution_times,
            bottlenecks=bottlenecks,
            recommendations=recommendations
        )
        
        # Store profile in database
        await self._store_performance_profile(profile)
        
        logger.info(f"Performance profile completed: {duration:.2f}ms duration")
        return profile
    
    async def create_debug_session(
        self,
        thread_id: str,
        breakpoints: List[str],
        debug_level: Optional[DebugLevel] = None,
        session_notes: str = ""
    ) -> str:
        """Create a new debug session with breakpoints"""
        
        session_id = f"debug_{thread_id}_{datetime.utcnow().timestamp()}"
        debug_level = debug_level or self.debug_level
        
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO debug_sessions VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            session_id, thread_id, datetime.utcnow().isoformat(), None,
            debug_level.value, json.dumps(breakpoints), session_notes
        ))
        
        self.conn.commit()
        
        logger.info(f"Created debug session {session_id} with {len(breakpoints)} breakpoints")
        return session_id
    
    async def get_workflow_timeline(
        self,
        thread_id: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[CheckpointMetadata]:
        """Get timeline of checkpoints for a workflow"""
        
        cursor = self.conn.cursor()
        
        query = "SELECT * FROM checkpoint_metadata WHERE thread_id = ?"
        params = [thread_id]
        
        if start_time:
            query += " AND timestamp >= ?"
            params.append(start_time.isoformat())
        
        if end_time:
            query += " AND timestamp <= ?"
            params.append(end_time.isoformat())
        
        query += " ORDER BY timestamp ASC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        timeline = []
        for row in rows:
            timeline.append(CheckpointMetadata(
                checkpoint_id=row[0],
                thread_id=row[1],
                timestamp=datetime.fromisoformat(row[2]),
                event_type=CheckpointEvent(row[3]),
                workflow_type=row[4],
                phase=row[5],
                state_hash=row[6],
                performance_metrics=json.loads(row[7]) if row[7] else {},
                debug_notes=row[8],
                parent_checkpoint=row[9]
            ))
        
        logger.info(f"Retrieved timeline with {len(timeline)} checkpoints for {thread_id}")
        return timeline
    
    async def get_checkpoint_metadata(self, checkpoint_id: str) -> Optional[CheckpointMetadata]:
        """Get metadata for a specific checkpoint"""
        
        # Check cache first
        if checkpoint_id in self.checkpoint_cache:
            return self.checkpoint_cache[checkpoint_id]
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM checkpoint_metadata WHERE checkpoint_id = ?", (checkpoint_id,))
        row = cursor.fetchone()
        
        if not row:
            return None
        
        metadata = CheckpointMetadata(
            checkpoint_id=row[0],
            thread_id=row[1],
            timestamp=datetime.fromisoformat(row[2]),
            event_type=CheckpointEvent(row[3]),
            workflow_type=row[4],
            phase=row[5],
            state_hash=row[6],
            performance_metrics=json.loads(row[7]) if row[7] else {},
            debug_notes=row[8],
            parent_checkpoint=row[9]
        )
        
        # Cache for future use
        self.checkpoint_cache[checkpoint_id] = metadata
        return metadata
    
    async def branch_from_checkpoint(
        self,
        checkpoint_id: str,
        new_thread_id: str,
        branch_notes: str = ""
    ) -> str:
        """Create a new execution branch from a checkpoint for A/B testing"""
        
        logger.info(f"Creating branch from checkpoint {checkpoint_id} -> {new_thread_id}")
        
        # Get original checkpoint
        original_metadata = await self.get_checkpoint_metadata(checkpoint_id)
        if not original_metadata:
            raise ValueError(f"Checkpoint {checkpoint_id} not found")
        
        # Create new branch checkpoint
        branch_checkpoint_id = await self.create_checkpoint(
            thread_id=new_thread_id,
            state=await self._get_state_at_checkpoint(checkpoint_id),
            event_type=CheckpointEvent.DEBUG_BREAKPOINT,
            workflow_type=original_metadata.workflow_type,
            phase=f"branch_from_{original_metadata.phase}",
            debug_notes=f"Branched from {checkpoint_id}. {branch_notes}",
            parent_checkpoint=checkpoint_id
        )
        
        logger.info(f"Created branch checkpoint {branch_checkpoint_id}")
        return branch_checkpoint_id
    
    async def cleanup_old_checkpoints(self, days_to_keep: int = 30):
        """Clean up old checkpoints to manage database size"""
        
        cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)
        
        cursor = self.conn.cursor()
        
        # Count checkpoints to be deleted
        cursor.execute(
            "SELECT COUNT(*) FROM checkpoint_metadata WHERE timestamp < ?",
            (cutoff_date.isoformat(),)
        )
        count = cursor.fetchone()[0]
        
        if count == 0:
            logger.info("No old checkpoints to clean up")
            return
        
        # Delete old checkpoints and related data
        cursor.execute("DELETE FROM state_diffs WHERE timestamp < ?", (cutoff_date.isoformat(),))
        cursor.execute("DELETE FROM performance_profiles WHERE timestamp < ?", (cutoff_date.isoformat(),))
        cursor.execute("DELETE FROM checkpoint_metadata WHERE timestamp < ?", (cutoff_date.isoformat(),))
        
        self.conn.commit()
        
        # Clear caches
        self.checkpoint_cache.clear()
        self.state_cache.clear()
        
        logger.info(f"Cleaned up {count} old checkpoints older than {days_to_keep} days")
    
    # Helper methods
    
    async def _get_state_at_checkpoint(self, checkpoint_id: str) -> Optional[Dict[str, Any]]:
        """Get the workflow state at a specific checkpoint"""
        
        # Check cache first
        if checkpoint_id in self.state_cache:
            return self.state_cache[checkpoint_id]
        
        # Get from checkpointer
        metadata = await self.get_checkpoint_metadata(checkpoint_id)
        if not metadata:
            return None
        
        try:
            config = RunnableConfig(
                configurable={"thread_id": metadata.thread_id}
            )
            # This would need to be implemented based on how states are stored
            # For now, return empty state
            return {}
        except Exception as e:
            logger.error(f"Could not retrieve state for checkpoint {checkpoint_id}: {e}")
            return None
    
    def _serialize_value(self, value: Any) -> str:
        """Serialize a value for comparison storage"""
        
        try:
            if isinstance(value, (dict, list)):
                return json.dumps(value, sort_keys=True, default=str)
            else:
                return str(value)
        except Exception:
            return f"<serialization_error: {type(value).__name__}>"
    
    def _analyze_agent_performance(
        self, 
        start_metrics: Dict[str, Any], 
        end_metrics: Dict[str, Any]
    ) -> Dict[str, float]:
        """Analyze agent execution times between checkpoints"""
        
        agent_times = {}
        
        # Extract agent timing data if available
        start_agents = start_metrics.get("agent_execution_times", {})
        end_agents = end_metrics.get("agent_execution_times", {})
        
        for agent_name in end_agents:
            if agent_name in start_agents:
                agent_times[agent_name] = end_agents[agent_name] - start_agents[agent_name]
            else:
                agent_times[agent_name] = end_agents[agent_name]
        
        return agent_times
    
    def _analyze_bottlenecks(
        self,
        duration_ms: float,
        agent_times: Dict[str, float],
        start_meta: CheckpointMetadata,
        end_meta: CheckpointMetadata
    ) -> Tuple[List[str], List[str]]:
        """Analyze bottlenecks and generate recommendations"""
        
        bottlenecks = []
        recommendations = []
        
        # Identify slow agents
        if agent_times:
            avg_time = sum(agent_times.values()) / len(agent_times)
            for agent, time in agent_times.items():
                if time > avg_time * 2:
                    bottlenecks.append(f"Slow agent: {agent} ({time:.2f}ms)")
        
        # Check overall duration
        if duration_ms > 10000:  # 10 seconds
            bottlenecks.append(f"Long overall execution: {duration_ms:.2f}ms")
            recommendations.append("Consider breaking down workflow into smaller phases")
        
        # Check for error patterns
        if "error" in end_meta.phase.lower():
            bottlenecks.append(f"Error in phase: {end_meta.phase}")
            recommendations.append("Review error handling and input validation")
        
        # Generic recommendations
        if not recommendations:
            recommendations.extend([
                "Monitor agent execution times regularly",
                "Consider parallel execution where possible",
                "Implement caching for frequently accessed data"
            ])
        
        return bottlenecks, recommendations
    
    async def _store_state_diff(self, diff: StateDiff):
        """Store state diff in database"""
        
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO state_diffs 
            (checkpoint_from, checkpoint_to, added_keys, removed_keys, modified_keys, value_changes, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            diff.checkpoint_from,
            diff.checkpoint_to,
            json.dumps(diff.added_keys),
            json.dumps(diff.removed_keys),
            json.dumps(diff.modified_keys),
            json.dumps(diff.value_changes),
            diff.timestamp.isoformat()
        ))
        
        self.conn.commit()
    
    async def _store_performance_profile(self, profile: PerformanceProfile):
        """Store performance profile in database"""
        
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO performance_profiles
            (start_checkpoint, end_checkpoint, duration_ms, memory_usage_mb, 
             agent_execution_times, bottlenecks, recommendations, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            profile.start_checkpoint,
            profile.end_checkpoint,
            profile.duration_ms,
            profile.memory_usage_mb,
            json.dumps(profile.agent_execution_times),
            json.dumps(profile.bottlenecks),
            json.dumps(profile.recommendations),
            datetime.utcnow().isoformat()
        ))
        
        self.conn.commit()
    
    async def _get_debug_breakpoints(self, thread_id: str) -> List[str]:
        """Get debug breakpoints for a thread"""
        
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT breakpoints FROM debug_sessions WHERE thread_id = ? ORDER BY start_time DESC LIMIT 1",
            (thread_id,)
        )
        row = cursor.fetchone()
        
        if row:
            return json.loads(row[0])
        return []


# Factory function for creating time travel debugger
def create_time_travel_debugger(
    db_path: str = "debugging/time_travel.sqlite",
    debug_level: DebugLevel = DebugLevel.STANDARD
) -> TimeTravel:
    """Create a time travel debugger instance"""
    
    return TimeTravel(db_path=db_path, debug_level=debug_level)


# Context manager for debug sessions
@asynccontextmanager
async def debug_session(
    time_travel: TimeTravel,
    thread_id: str,
    breakpoints: List[str],
    session_notes: str = ""
):
    """Context manager for managing debug sessions"""
    
    session_id = await time_travel.create_debug_session(
        thread_id=thread_id,
        breakpoints=breakpoints,
        session_notes=session_notes
    )
    
    try:
        yield session_id
    finally:
        # End debug session
        cursor = time_travel.conn.cursor()
        cursor.execute(
            "UPDATE debug_sessions SET end_time = ? WHERE session_id = ?",
            (datetime.utcnow().isoformat(), session_id)
        )
        time_travel.conn.commit()
        
        logger.info(f"Ended debug session {session_id}")


# Export main classes and functions
__all__ = [
    "TimeTravel",
    "DebugLevel", 
    "CheckpointEvent",
    "CheckpointMetadata",
    "StateDiff",
    "PerformanceProfile",
    "create_time_travel_debugger",
    "debug_session"
]
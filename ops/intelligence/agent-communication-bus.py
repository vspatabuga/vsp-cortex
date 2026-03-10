#!/usr/bin/env python3
"""
Agent Communication Bus
Component: AGENT-COORD (Phase 3)
Purpose: Message broker untuk komunikasi multi-agent

Implements: vsp-agent-protocol/1.0
"""

import json
import queue
import threading
import time
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
from enum import Enum
from datetime import datetime
import hashlib


class MessageType(Enum):
    TASK_REQUEST = "task_request"
    TASK_ASSIGNMENT = "task_assignment"
    STATUS_UPDATE = "status_update"
    TASK_COMPLETE = "task_complete"
    TASK_FAILED = "task_failed"
    ERROR = "error"


class Priority(Enum):
    CRITICAL = 0
    HIGH = 1
    NORMAL = 2
    LOW = 3


@dataclass
class Agent:
    """Agent profile"""
    id: str
    name: str
    capabilities: List[str]
    status: str = "ready"
    load: int = 0
    max_parallelism: int = 5

    def is_available(self) -> bool:
        return self.status == "ready" and self.load < self.max_parallelism


@dataclass
class Message:
    """vsp-agent-protocol message"""
    type: str
    from_agent: str
    to_agent: str
    timestamp: str
    priority: int = Priority.NORMAL.value
    payload: Dict = None
    message_id: Optional[str] = None

    def __post_init__(self):
        if self.message_id is None:
            msg_str = f"{self.from_agent}:{self.to_agent}:{self.timestamp}"
            self.message_id = hashlib.md5(msg_str.encode()).hexdigest()[:12]

    def to_json(self) -> str:
        data = asdict(self)
        data['priority'] = self.priority
        return json.dumps(data, indent=2)


class AgentCommunicationBus:
    """Message broker untuk koordinasi multi-agent"""

    def __init__(self, log_file: str = "/home/vsp/vsp-cortex/log/agent-communication.log"):
        self.agents: Dict[str, Agent] = {}
        self.message_queue: queue.PriorityQueue = queue.PriorityQueue()
        self.log_file = log_file
        self.running = False
        self.message_history: List[Message] = []
        self.stats = {
            "messages_processed": 0,
            "tasks_completed": 0,
            "tasks_failed": 0,
            "conflicts_detected": 0,
        }

    def register_agent(self, agent: Agent):
        """Register agent ke sistem"""
        self.agents[agent.id] = agent
        self._log(f"Agent registered: {agent.id} ({agent.name})")

    def _log(self, message: str):
        """Log ke file"""
        timestamp = datetime.utcnow().isoformat()
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)
        with open(self.log_file, "a") as f:
            f.write(log_msg + "\n")

    def send_message(self, msg: Message):
        """Enqueue message dengan priority"""
        self.message_queue.put((msg.priority, msg))
        self._log(f"Message queued: {msg.message_id} ({msg.type})")

    def process_messages(self):
        """Process message queue"""
        while self.running:
            try:
                priority, msg = self.message_queue.get(timeout=1)
                self._process_single_message(msg)
                self.stats["messages_processed"] += 1
            except queue.Empty:
                continue
            except Exception as e:
                self._log(f"ERROR processing message: {str(e)}")

    def _process_single_message(self, msg: Message):
        """Process single message"""
        self._log(f"Processing: {msg.type} from {msg.from_agent} to {msg.to_agent}")
        self.message_history.append(msg)

        # Route message berdasarkan type
        if msg.type == MessageType.TASK_REQUEST.value:
            self._handle_task_request(msg)
        elif msg.type == MessageType.STATUS_UPDATE.value:
            self._handle_status_update(msg)
        elif msg.type == MessageType.TASK_COMPLETE.value:
            self._handle_task_complete(msg)
        elif msg.type == MessageType.TASK_FAILED.value:
            self._handle_task_failed(msg)

    def _handle_task_request(self, msg: Message):
        """Handle task request"""
        task_id = msg.payload.get("task_id", "UNKNOWN")
        # Assign to available agent
        target_agent = self._find_available_agent(msg.payload.get("required_capabilities", []))
        if target_agent:
            target_agent.load += 1
            self._log(f"Task {task_id} assigned to {target_agent.id}")
        else:
            self._log(f"WARNING: No available agent for task {task_id}")
            self.stats["conflicts_detected"] += 1

    def _handle_status_update(self, msg: Message):
        """Handle status update"""
        task_id = msg.payload.get("task_id", "UNKNOWN")
        progress = msg.payload.get("progress", 0)
        self._log(f"Task {task_id}: {progress}%")

    def _handle_task_complete(self, msg: Message):
        """Handle task completion"""
        task_id = msg.payload.get("task_id", "UNKNOWN")
        agent_id = msg.from_agent
        if agent_id in self.agents:
            self.agents[agent_id].load = max(0, self.agents[agent_id].load - 1)
        self.stats["tasks_completed"] += 1
        self._log(f"Task {task_id} completed by {agent_id}")

    def _handle_task_failed(self, msg: Message):
        """Handle task failure"""
        task_id = msg.payload.get("task_id", "UNKNOWN")
        agent_id = msg.from_agent
        if agent_id in self.agents:
            self.agents[agent_id].load = max(0, self.agents[agent_id].load - 1)
        self.stats["tasks_failed"] += 1
        self._log(f"Task {task_id} FAILED in {agent_id}")

    def _find_available_agent(self, required_capabilities: List[str]) -> Optional[Agent]:
        """Find available agent dengan required capabilities"""
        for agent in self.agents.values():
            if agent.is_available():
                if not required_capabilities or any(cap in agent.capabilities for cap in required_capabilities):
                    return agent
        return None

    def start(self):
        """Start message processor"""
        self.running = True
        processor_thread = threading.Thread(target=self.process_messages, daemon=True)
        processor_thread.start()
        self._log("Agent Communication Bus started")

    def stop(self):
        """Stop message processor"""
        self.running = False
        self._log("Agent Communication Bus stopped")

    def get_status(self) -> Dict:
        """Get system status"""
        return {
            "agents": {aid: {"status": a.status, "load": a.load} for aid, a in self.agents.items()},
            "stats": self.stats,
            "queue_size": self.message_queue.qsize(),
        }


# Example usage & initialization
if __name__ == "__main__":
    print("=== VSP-Cortex Agent Communication Bus ===\n")

    # Initialize bus
    bus = AgentCommunicationBus()

    # Register agents
    agents = [
        Agent(id="copilot", name="Copilot CLI", capabilities=["code_execution", "git_operations"]),
        Agent(id="gemini", name="Gemini CLI", capabilities=["experimentation", "data_analysis"]),
        Agent(id="operator", name="Operator VSP", capabilities=["approval", "override"]),
    ]

    for agent in agents:
        bus.register_agent(agent)

    # Start bus
    bus.start()

    # Simulate task requests
    print("\n--- Simulating Task Requests ---\n")
    
    task_msg = Message(
        type=MessageType.TASK_REQUEST.value,
        from_agent="operator",
        to_agent="decision_engine",
        timestamp=datetime.utcnow().isoformat(),
        priority=Priority.HIGH.value,
        payload={
            "task_id": "TASK-001",
            "action": "clone_logseq",
            "required_capabilities": ["code_execution"],
        }
    )
    bus.send_message(task_msg)

    # Wait a bit for processing
    time.sleep(2)

    # Print status
    print("\n--- System Status ---")
    status = bus.get_status()
    print(json.dumps(status, indent=2))

    # Cleanup
    bus.stop()
    print("\nAgent Communication Bus ready for deployment")

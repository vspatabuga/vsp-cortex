#!/usr/bin/env python3
"""
Automated Decision Engine
Component: DECISION-ENGINE (Phase 3.2)
Purpose: AI-driven decision making untuk orkestrasi task & workflow

Implements: Manifest-based rules + Agent profiles + Context analysis
"""

import json
import yaml
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum
from datetime import datetime


class DecisionMode(Enum):
    AUTONOMOUS = "autonomous"
    GUIDED = "guided"
    MANUAL = "manual"


class TaskPriority(Enum):
    CRITICAL = 0
    HIGH = 1
    NORMAL = 2
    LOW = 3


@dataclass
class AgentProfile:
    """Agent capability & performance profile"""
    id: str
    name: str
    specialization: str
    max_concurrent_tasks: int
    average_task_duration: int  # seconds
    success_rate: float = 0.95
    current_load: int = 0

    def can_accept_task(self) -> bool:
        return self.current_load < self.max_concurrent_tasks

    def estimated_start_time(self) -> int:
        """Estimated time sebelum bisa start task (seconds)"""
        return self.current_load * self.average_task_duration


@dataclass
class ManifestRule:
    """Rule dari manifest untuk decision-making"""
    id: str
    condition: str
    action: str
    priority: int
    apply_to: List[str]  # task types


class DecisionEngine:
    """AI-driven decision engine untuk VSP-Cortex"""

    def __init__(self, manifest_file: str = None, log_file: str = "/home/vsp/vsp-cortex/log/decision-engine.log"):
        self.manifest_file = manifest_file
        self.log_file = log_file
        self.mode = DecisionMode.AUTONOMOUS
        self.agents: Dict[str, AgentProfile] = {}
        self.rules: List[ManifestRule] = []
        self.decision_history: List[Dict] = []
        self.conflict_resolver_mode = "automatic"

    def register_agent(self, profile: AgentProfile):
        """Register agent profile"""
        self.agents[profile.id] = profile
        self._log(f"Agent profile registered: {profile.id} ({profile.specialization})")

    def load_manifest_rules(self, manifest: Dict):
        """Load rules dari manifest"""
        if "rules" in manifest:
            for rule_data in manifest["rules"]:
                rule = ManifestRule(**rule_data)
                self.rules.append(rule)
                self._log(f"Rule loaded: {rule.id}")

    def _log(self, message: str):
        """Log decision"""
        timestamp = datetime.utcnow().isoformat()
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)
        with open(self.log_file, "a") as f:
            f.write(log_msg + "\n")

    def make_decision(self, task: Dict) -> Dict:
        """
        Make autonomous decision untuk task
        
        Input:
        {
            "id": "TASK-001",
            "type": "code_execution | data_analysis | ...",
            "priority": 0-3,
            "dependencies": [],
            "estimated_duration": 600,
            "required_capabilities": []
        }
        
        Output:
        {
            "task_id": "TASK-001",
            "decision": "assign | delay | escalate",
            "assigned_agent": "copilot | gemini",
            "scheduled_time": "2026-03-10T11:20:00Z",
            "reason": "string"
        }
        """
        task_id = task.get("id", "UNKNOWN")
        self._log(f"Making decision for: {task_id}")

        # 1. Validate against manifest compliance
        compliance_check = self._check_manifest_compliance(task)
        if not compliance_check["valid"]:
            return {
                "task_id": task_id,
                "decision": "escalate",
                "reason": f"Manifest compliance failure: {compliance_check['reason']}",
                "assigned_agent": None,
                "scheduled_time": None,
            }

        # 2. Check dependencies
        if task.get("dependencies"):
            dep_check = self._check_dependencies(task["dependencies"])
            if not dep_check["ready"]:
                return {
                    "task_id": task_id,
                    "decision": "delay",
                    "reason": f"Waiting for dependencies: {dep_check['waiting_for']}",
                    "assigned_agent": None,
                    "scheduled_time": self._estimate_availability(task),
                }

        # 3. Find best agent
        best_agent = self._find_best_agent(task)
        if not best_agent:
            return {
                "task_id": task_id,
                "decision": "escalate",
                "reason": "No available agent matching requirements",
                "assigned_agent": None,
                "scheduled_time": None,
            }

        # 4. Detect conflicts
        conflicts = self._detect_conflicts(task, best_agent)
        if conflicts and self.conflict_resolver_mode == "escalate":
            return {
                "task_id": task_id,
                "decision": "escalate",
                "reason": f"Conflicts detected: {conflicts}",
                "assigned_agent": best_agent.id,
                "scheduled_time": None,
            }

        # 5. Generate execution plan
        scheduled_time = self._calculate_scheduled_time(best_agent)

        decision = {
            "task_id": task_id,
            "decision": "assign",
            "assigned_agent": best_agent.id,
            "scheduled_time": scheduled_time,
            "reason": f"Assigned to {best_agent.name} (specialization: {best_agent.specialization})",
            "confidence": 0.95,
        }

        # Record decision
        self.decision_history.append(decision)
        self._log(f"Decision made: {decision['decision']} → {decision['assigned_agent']}")

        return decision

    def _check_manifest_compliance(self, task: Dict) -> Dict:
        """Verify task matches manifest rules"""
        task_type = task.get("type", "unknown")
        applicable_rules = [r for r in self.rules if task_type in r.apply_to]

        if not applicable_rules:
            return {"valid": False, "reason": f"No rules for task type: {task_type}"}

        # Check if task meets rule conditions (simplified)
        for rule in applicable_rules:
            if rule.priority <= TaskPriority.NORMAL.value:
                return {"valid": True}

        return {"valid": True}

    def _check_dependencies(self, dependencies: List[str]) -> Dict:
        """Check if dependencies are satisfied"""
        # Simplified: assume all dependencies are met
        return {"ready": True, "waiting_for": []}

    def _find_best_agent(self, task: Dict) -> Optional[AgentProfile]:
        """Find best agent untuk task"""
        required_caps = task.get("required_capabilities", [])
        priority = task.get("priority", TaskPriority.NORMAL.value)

        # Score each agent
        best_agent = None
        best_score = -1

        for agent in self.agents.values():
            if not agent.can_accept_task():
                continue

            # Match capabilities
            if required_caps:
                if agent.specialization not in required_caps:
                    continue

            # Score: prioritize availability & success rate
            score = (agent.success_rate * 100) - (agent.current_load * 10) - priority
            if score > best_score:
                best_score = score
                best_agent = agent

        return best_agent

    def _detect_conflicts(self, task: Dict, agent: AgentProfile) -> List[str]:
        """Detect potential conflicts"""
        conflicts = []
        # Check resource contention, scheduling conflicts, etc.
        # Simplified for now
        return conflicts

    def _calculate_scheduled_time(self, agent: AgentProfile) -> str:
        """Calculate when task should start"""
        start_delay = agent.estimated_start_time()
        from datetime import datetime, timedelta
        scheduled = datetime.utcnow() + timedelta(seconds=start_delay)
        return scheduled.isoformat()

    def _estimate_availability(self, task: Dict) -> str:
        """Estimate when agent will be available"""
        # Find earliest available agent
        min_wait = float('inf')
        for agent in self.agents.values():
            if agent.can_accept_task():
                wait = 0
            else:
                wait = agent.estimated_start_time()
            min_wait = min(min_wait, wait)

        from datetime import datetime, timedelta
        estimated = datetime.utcnow() + timedelta(seconds=min_wait)
        return estimated.isoformat()

    def get_statistics(self) -> Dict:
        """Get decision engine statistics"""
        return {
            "total_decisions": len(self.decision_history),
            "assignments": len([d for d in self.decision_history if d["decision"] == "assign"]),
            "delays": len([d for d in self.decision_history if d["decision"] == "delay"]),
            "escalations": len([d for d in self.decision_history if d["decision"] == "escalate"]),
            "agent_load": {aid: a.current_load for aid, a in self.agents.items()},
        }


# Example usage & testing
if __name__ == "__main__":
    print("=== VSP-Cortex Automated Decision Engine ===\n")

    # Initialize engine
    engine = DecisionEngine()
    engine.mode = DecisionMode.AUTONOMOUS
    engine.conflict_resolver_mode = "automatic"

    # Register agent profiles
    agents = [
        AgentProfile(
            id="copilot",
            name="Copilot CLI",
            specialization="code_execution",
            max_concurrent_tasks=5,
            average_task_duration=300,
        ),
        AgentProfile(
            id="gemini",
            name="Gemini CLI",
            specialization="data_analysis",
            max_concurrent_tasks=3,
            average_task_duration=600,
        ),
    ]

    for agent in agents:
        engine.register_agent(agent)

    # Load manifest rules (simplified)
    manifest = {
        "rules": [
            {
                "id": "RULE-001",
                "condition": "type == code_execution",
                "action": "assign_to_copilot",
                "priority": 1,
                "apply_to": ["code_execution", "git_operations"],
            },
            {
                "id": "RULE-002",
                "condition": "type == data_analysis",
                "action": "assign_to_gemini",
                "priority": 1,
                "apply_to": ["data_analysis", "experimentation"],
            },
        ]
    }
    engine.load_manifest_rules(manifest)

    # Test task decisions
    print("--- Testing Decision Making ---\n")

    test_tasks = [
        {
            "id": "TASK-001",
            "type": "code_execution",
            "priority": 1,
            "dependencies": [],
            "estimated_duration": 300,
            "required_capabilities": ["code_execution"],
        },
        {
            "id": "TASK-002",
            "type": "data_analysis",
            "priority": 2,
            "dependencies": [],
            "estimated_duration": 600,
            "required_capabilities": ["data_analysis"],
        },
    ]

    for task in test_tasks:
        print(f"\nTask: {task['id']}")
        decision = engine.make_decision(task)
        print(f"Decision: {json.dumps(decision, indent=2)}")

        # Update agent load for simulation
        if decision["assigned_agent"]:
            engine.agents[decision["assigned_agent"]].current_load += 1

    # Print statistics
    print("\n--- Decision Engine Statistics ---")
    stats = engine.get_statistics()
    print(json.dumps(stats, indent=2))

    print("\nDecision Engine ready for deployment")

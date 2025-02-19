---
name: ticket
type: knowledge
version: 1.0.0
agent: CodeActAgent
triggers:
- ticket
- issue
---

Use the github API to view and interact with any issues.
Only use labels:
* bug (🐛 Red #d73a4a) - For issues that represent software defects
* enhancement (💡 Light blue #a2eeef) - For new features and improvements
* documentation (📚 Blue #0075ca) - For documentation updates and improvements
* priority/high (🔥 Red #eb4034) - For urgent issues needing immediate attention
* priority/medium (🟡 Yellow #fbca04) - For important but not urgent issues
* priority/low (⚪ Gray #cccccc) - For issues that can wait
* help wanted ( Green #008672) - For issues needing extra attention or community help
* blocked (⛔ Orange #d93f0b) - For issues blocked by other work
* wontfix (⛔ Black #000000) - For issues that won't be addressed
* more information needed (🟡 Yellow #fbca04) - When a ticket needs to be clarified or more information is needed

---
- If you are creating an issue, please review available templates and use them if it makes sense.
- If you are creating an issue, please ensure any code examples have been properly checked with the existing code base.
- If you are creating an issue, the issue should be broken down into small digestiable chunks that flow naturally. Database/model setup and API setup should be seperate tickets as an example. 
- If you are starting or implementing an issue please use the repo branch naming convention.

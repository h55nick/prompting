---
name: update_knowledge
type: knowledge
version: 1.0.0
agent: CodeActAgent
triggers:
- uknowledge
---

You have been requested to update knowledge. Knowledge is found in `.openhands/microagents/knowledge/*`

Please find the relevant knowledge file, or create a new one with the correct header. Example:
```
---
name: update_knowledge
type: knowledge
version: 1.0.0
agent: CodeActAgent
triggers:
- update knowledge
---
```

The knowledge should be specific and concise. 
If you are asked to use best-practices please cite your sources.
You should ask any clarifying questions about any knowledge you are adding to ensure it is accurate.

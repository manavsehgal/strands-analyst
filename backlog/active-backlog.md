# Active Backlog

[x] Fix the deprecation warning that occurs when I quit the `analystai` CLI.
🗣️  You: quit
👋 Thank you for using Analyst Chat. Goodbye!
<sys>:0: DeprecationWarning: builtin type swigvarlink has no __module__ attribute

**Completion Summary:** Fixed the swigvarlink deprecation warning by implementing comprehensive warning suppression in the CLI. The solution involved:
1. Enhanced `analyst/utils/shell_wrapper.py` with a new `suppress_swigvarlink_warning()` function to filter SWIG-wrapped C extension warnings
2. Updated `analyst/cli/chat.py` with early warning suppression, global deprecation warning filtering, and an atexit handler to ensure warnings remain suppressed throughout the program lifecycle
3. The fix addresses warnings from SWIG-based dependencies (likely PyMuPDF) that occur during Python's cleanup phase when exiting the CLI
4. Verified that the warning no longer appears when quitting the `analystai` CLI

[x] When `analystai` quits the Thank You message should be: 
"Thank you for using Strands Analyst AI. Hope you found it useful."
"Noticed an issue? Please report here https://github.com/manavsehgal/strands-analyst/issues"

**Completion Summary:** Updated the goodbye messages in the `analystai` CLI to provide a more informative and branded exit experience. The changes involved:
1. Replaced all goodbye messages in `analyst/cli/chat.py` at three locations (lines 149, 189, 194)
2. Updated the main quit message from "Thank you for using Analyst Chat. Goodbye!" to the new two-line format
3. Enhanced KeyboardInterrupt (Ctrl+C) and EOFError (Ctrl+D) handlers with the same consistent messaging
4. Added GitHub issues link to encourage user feedback and bug reporting
5. Verified the new messages display correctly when exiting the CLI with the "quit" command

[ ] Review existing caching capabilities within the project. Create comprehensive message-level caching system for conversation continuity in chat agents, including cache invalidation strategies, hit/miss metrics monitoring, and request-level caching for repeated tool operations. Read https://strandsagents.com/latest/documentation/docs/user-guide/concepts/model-providers/amazon-bedrock/#caching and other Strands Agents docs to understand if this is model provider specific feature or generalized across providers.

[ ] Integrate OpenTelemetry for standardized instrumentation with trace collection for model and tool invocations, comprehensive performance dashboards, automated alerts for performance degradation, and user interaction feedback metrics.

[ ] Optimize tool execution performance with intelligent context-based tool selection, concurrent execution for independent operations via ToolExecutor, lazy initialization for tool loading, and tool result caching for expensive operations.

[ ] Implement real-time cost optimization framework with per-agent cost tracking, budgeting and alerting mechanisms, cost-aware model selection, token usage optimization recommendations, and cost analysis reporting dashboards.

[ ] Enhance security guardrails with advanced prompt injection defense patterns, structured input validation with clear section delimiters, adversarial example detection, Bedrock guardrails integration, and security audit trails for sensitive operations.

[ ] Create automated quality assurance system with agent behavior consistency testing, performance regression testing, output quality scoring, A/B testing framework for agent improvements, and continuous evaluation pipelines.

[ ] Build multi-agent orchestration framework implementing the agents-as-tools pattern with workflow management, dependency tracking, concurrent tool execution, and agent specialization for domain-specific tasks.


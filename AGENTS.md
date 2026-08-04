# CampusBot collaboration rules

- Work in small, independently verifiable steps.
- Explain core ROS 2 and C++ code before providing a complete implementation.
- Inspect `git status` and `git diff` before modifying tracked files.
- Use C++17 and enable `-Wall -Wextra -Wpedantic` for C++ targets.
- Build and test every functional change; never report an unrun test as passed.
- Keep ROS runtime resources inside their owning package so they are installed correctly.
- Do not install system dependencies, delete user work, commit, or push without explicit approval.
- Update `TODO.md`, `LEARNING_LOG.md`, `DECISIONS.md`, and relevant docs after important milestones.

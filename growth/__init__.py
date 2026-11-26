"""Channel growth + monetization readiness system for the Shorts pipeline.

Seven independent validators (topic, originality, copyright/policy, metadata, subscriber conversion,
performance, monetization readiness), a per-video decision, a channel status, and a dashboard with history.

Read-only by design: it never uploads, edits, publishes or deletes anything on YouTube. Every number it shows
comes from local files, the official YouTube Data/Analytics APIs, or a Studio export the user filled in.
Missing data is reported as missing, never estimated.

Entry point: story-pipeline/growth.py (python growth.py --help).
"""

# Issue Tracker

This repo uses GitHub Issues as the default issue tracker.

Remote:

- `origin`: `https://github.com/oADAo/writing-agent`

Use the `gh` CLI from inside `X:\writing-agent`; `gh` can infer the repo from the remote.

## Common Commands

Create an issue:

```powershell
gh issue create --title "..." --body "..."
```

Read an issue:

```powershell
gh issue view <number> --comments
```

List open issues:

```powershell
gh issue list --state open --json number,title,body,labels,comments
```

Comment:

```powershell
gh issue comment <number> --body "..."
```

Apply a label:

```powershell
gh issue edit <number> --add-label "needs-triage"
```

Close:

```powershell
gh issue close <number> --comment "..."
```

## When A Skill Says "Publish To The Issue Tracker"

Create a GitHub issue unless the user explicitly says to keep the plan local.

## When A Skill Says "Fetch The Relevant Ticket"

Use `gh issue view <number> --comments` and summarize the request before changing files.

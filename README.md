# Reusable OpenAI Fine Tune
> Use this codebase to fine tune OpenAI models with your own data.

## Setup
- Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Install dependencies `uv sync`
- Set your OpenAI API key as an environment variable `export OPENAI_API_KEY=<your_api_key>`

## Fine-Tune Process Example Commands
- `uv run finetune upload-dataset datasets/example-sarcastic-factbot.jsonl` - Upload a the example dataset to the fine-tune API
- `uv run finetune list-files` - List all files uploaded for fine-tuning. You should see `example-sarcastic-factbot.jsonl`
- `uv run finetune train-model example-sarcastic-factbot.jsonl --model gpt-4o-2024-08-06` - Train a fine tuned model given the example dataset and base model
- `uv run finetune list-jobs` - List all fine-tune jobs. You should see your job in the list
- `uv run finetune fine-tune-prompt <model_name> <prompt> [--system-message <system_message>]` - After model training, send a prompt to a fine-tuned model and get the response

## Commands

### Dataset File Management
- `uv run finetune list-files` - List all files uploaded for fine-tuning
- `uv run finetune delete-files-by-name <file_name>` - Delete all files that match the given name
- `uv run finetune upload-dataset <file_path>` - Upload a dataset to the fine-tune API

### Fine-Tune Model Training
- `uv run finetune list-jobs` - List all fine-tune jobs
- `uv run finetune train-model <file_name> [--model <model_name>]` - Start a fine-tuning job with the specified file and model
- `uv run finetune list-job-events <fine_tune_job_id>` - List the events for a fine-tuning job
- `uv run finetune retrieve-job <job_id>` - Retrieve the state of a fine-tuning job
- `uv run finetune cancel-job <job_id>` - Cancel a fine-tuning job

### Fine-Tune Prompting
- `uv run finetune fine-tune-prompt <model_name> <prompt> [--system-message <system_message>]` - Send a prompt to a fine-tuned model and get the response

## Tools + Resources
- [OpenAI Python](https://github.com/openai/openai-python)
- [OpenAI Fine-Tune API](https://platform.openai.com/docs/guides/fine-tuning)
- [OpenAI Fine-Tune Pricing](https://openai.com/api/pricing/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (hyper fast hyper modern python package manager - replaces pip, poetry, etc.)
- [typer](https://typer.tiangolo.com/) (python package for building CLI apps)

---

## When do I fine-tune?

### Common use cases
> Some common use cases where fine-tuning can improve results:

!(Add decision diagram here on when to fine-tune)[]

- Setting the style, tone, format, or other qualitative aspects
- Improving reliability at producing a desired output
- Correcting failures to follow complex prompts
- Handling many edge cases in specific ways
- Performing a new skill or task that’s hard to articulate in a prompt
- One high-level way to think about these cases is when it’s easier to "show, not tell". In the sections to come, we will explore how to set up data for fine-tuning and various examples where fine-tuning improves the performance over the baseline model.

- Another scenario where fine-tuning is effective is reducing cost and/or latency by replacing a more expensive model like gpt-4o with a fine-tuned gpt-4o-mini model. If you can achieve good results with gpt-4o, you can often reach similar quality with a fine-tuned gpt-4o-mini model by fine-tuning on the gpt-4o completions, possibly with a shortened instruction prompt.
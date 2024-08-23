import os
import sys
import typer
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = typer.Typer()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Fine-tunable OpenAI models
GPT_4o_2024_08_06 = "gpt-4o-2024-08-06"
GPT_4o_MINI_2024_07_18 = "gpt-4o-mini-2024-07-18"
GPT_4_0613 = "gpt-4-0613"
GPT_3_5_TURBO_0125 = "gpt-3.5-turbo-0125"
GPT_3_5_TURBO_1106 = "gpt-3.5-turbo-1106"
GPT_3_5_TURBO_0613 = "gpt-3.5-turbo-0613"


# ------------------------------ DATASET FILE MANAGEMENT ------------------------------


@app.command()
def list_files():
    """
    List all files uploaded for fine-tuning

    Usage:
    $ uv run finetune list-files
    """
    typer.echo("Listing files uploaded for fine-tuning...")
    files = client.files.list(purpose="fine-tune")
    if not files.data:
        typer.echo("No files found for fine-tuning.")
    else:
        for file in files:
            typer.echo(
                f"File ID: {file.id}, Filename: {file.filename}, Purpose: {file.purpose}, Created at: {file.created_at}"
            )


@app.command()
def delete_files_by_name(file_name: str):
    """
    Delete all files that match the given name

    Usage:
    $ uv run finetune delete-files-by-name example-sarcastic-factbot.jsonl
    """
    typer.echo(f"Searching for files matching: {file_name}")
    try:
        files = client.files.list(purpose="fine-tune")
        matching_files = [file for file in files.data if file.filename == file_name]

        if not matching_files:
            typer.echo(f"No files found matching '{file_name}'.")
            return

        for file in matching_files:
            client.files.delete(file.id)
            typer.echo(f"Deleted file: {file.filename} (ID: {file.id})")

        typer.echo(f"Deleted {len(matching_files)} file(s) matching '{file_name}'.")
    except Exception as e:
        typer.echo(f"Error deleting files: {str(e)}")


@app.command()
def upload_dataset(file_path: str):
    """
    Upload a dataset to the fine-tune API

    Usage:
    $ uv run finetune upload-dataset datasets/example-sarcastic-factbot.jsonl
    """
    typer.echo(f"Uploading dataset to fine-tune API...")
    try:
        with open(file_path, "rb") as file:
            response = client.files.create(file=file, purpose="fine-tune")
        typer.echo(f"File uploaded successfully. File ID: {response.id}")
    except Exception as e:
        typer.echo(f"Error uploading file: {str(e)}")


# ------------------------------ FINE-TUNE MODEL TRAINING ------------------------------


@app.command()
def list_jobs():
    """
    List all fine-tune jobs

    Usage:
    $ uv run finetune list-jobs
    """
    typer.echo(f"Listing fine-tune jobs...")
    jobs = client.fine_tuning.jobs.list()
    if not jobs.data:
        typer.echo("No fine-tuning jobs found.")
    else:
        for job in jobs:
            typer.echo(
                f"Job ID: {job.id}, Status: {job.status}, Model: {job.model}, Fine-funed Model: {job.fine_tuned_model}"
            )


@app.command()
def train_model(file_name: str, model: str = GPT_4o_MINI_2024_07_18):
    """
    Start a fine-tuning job with the specified file and model

    Usage:
    $ uv run finetune train-model example-sarcastic-factbot.jsonl --model gpt-4o-mini-2024-07-18
    """
    typer.echo(f"Searching for file: {file_name}")
    try:
        files = client.files.list(purpose="fine-tune")
        sorted_files = sorted(files.data, key=lambda x: x.created_at, reverse=True)
        matching_file = next(
            (file for file in sorted_files if file.filename == file_name), None
        )

        if matching_file:
            typer.echo(
                f"Starting fine-tuning job with file ID: {matching_file.id} and model: {model}"
            )
            job = client.fine_tuning.jobs.create(
                training_file=matching_file.id, model=model
            )
            typer.echo(f"Fine-tuning job created successfully. Job ID: {job.id}")
        else:
            typer.echo(f"Error: File '{file_name}' not found in fine-tune files.")
    except Exception as e:
        typer.echo(f"Error creating fine-tuning job: {str(e)}")


@app.command()
def list_job_events(fine_tune_job_id: str):
    """
    List the events for a fine-tuning job

    Usage:
    $ uv run finetune list-job-events ftjob-abc123

    Usage notes:
    - replace ftjob-abc123 with the ID of your fine-tuning job from the list-jobs command
    """
    typer.echo(f"Listing events for fine-tuning job: {fine_tune_job_id}")
    try:
        events = client.fine_tuning.jobs.list_events(
            fine_tuning_job_id=fine_tune_job_id
        )
        for event in events:
            typer.echo(f"[{event.created_at}] {event.level}: {event.message}")
    except Exception as e:
        typer.echo(f"Error listing job events: {str(e)}")


@app.command()
def retrieve_job(job_id: str):
    """
    Retrieve the state of a fine-tuning job

    Usage:
    $ uv run finetune retrieve-job ftjob-abc123

    Usage notes:
    - replace ftjob-abc123 with the ID of your fine-tuning job
    """
    typer.echo(f"Retrieving state for fine-tuning job: {job_id}")
    try:
        job = client.fine_tuning.jobs.retrieve(job_id)
        typer.echo(f"Job ID: {job.id}")
        typer.echo(f"Status: {job.status}")
        typer.echo(f"Model: {job.model}")
        typer.echo(f"Created at: {job.created_at}")
        typer.echo(f"Finished at: {job.finished_at}")
        typer.echo(f"Fine-tuned model: {job.fine_tuned_model}")
    except Exception as e:
        typer.echo(f"Error retrieving job state: {str(e)}")


@app.command()
def cancel_job(job_id: str):
    """
    Cancel a fine-tuning job

    Usage:
    $ uv run finetune cancel-job ftjob-abc123

    Usage notes:
    - replace ftjob-abc123 with the ID of your fine-tuning job
    - You can only cancel a job that is in the 'pending' or 'running' state
    """
    typer.echo(f"Cancelling fine-tuning job: {job_id}")
    try:
        job = client.fine_tuning.jobs.cancel(job_id)
        typer.echo(f"Job {job_id} has been cancelled.")
        typer.echo(f"Status: {job.status}")
    except Exception as e:
        typer.echo(f"Error cancelling job: {str(e)}")


# ------------------------------ FINE-TUNE PROMPTING ------------------------------


@app.command()
def fine_tune_prompt(model_name: str, prompt: str, system_message: str = ""):
    """
    Send a prompt to a fine-tuned model and get the response

    Usage:
    $ uv run finetune fine-tune-prompt ft:gpt-4o-mini-2024-07-18:my-org:custom_model:1234abcd "What's the capital of France?" --system-message "Marv is a factual chatbot that is also sarcastic."

    Usage notes:
    - replace ft... with the ID of your fine-tuning job from the list-jobs command
    - The system message is optional. If not provided, no system message will be sent.
    """
    typer.echo(f"Sending prompt to fine-tuned model: {model_name}")
    try:
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
        )
        typer.echo("Response from fine-tuned model:")
        typer.echo(response.choices[0].message.content)
    except Exception as e:
        typer.echo(f"Error prompting fine-tuned model: {str(e)}")


# ------------------------------ MAIN ------------------------------


def main():
    app()


if __name__ == "__main__":
    main()

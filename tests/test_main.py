from typer.testing import CliRunner
from task_cli.main import app
import pytest
from task_cli.service import add_task, get_tasks, delete_task, update_task

def test_add_command(tmp_path, monkeypatch):
    monkeypatch.setattr("task_cli.storage.DATA_FILE", tmp_path / "tasks.json")
    runner = CliRunner()
    result = runner.invoke(app, ["add", "Buy groceries"])
    assert result.exit_code == 0

def test_list_command(tmp_path, monkeypatch):
    monkeypatch.setattr("task_cli.storage.DATA_FILE", tmp_path / "tasks.json")
    runner = CliRunner()
    add_task("Buy groceries")
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "Buy groceries" in result.output
    assert "todo" in result.output
    assert "1" in result.output

def test_delete_command(tmp_path, monkeypatch):
    monkeypatch.setattr("task_cli.storage.DATA_FILE", tmp_path / "tasks.json")
    runner = CliRunner()
    add_task("Buy groceries")
    result = runner.invoke(app, ["delete", "1"])
    assert result.exit_code == 0

def test_update_command(tmp_path, monkeypatch):
    monkeypatch.setattr("task_cli.storage.DATA_FILE", tmp_path / "tasks.json")
    runner = CliRunner()
    add_task("Buy groceries")
    result = runner.invoke(app, ["update", "1", "--description", "Updated groceries"])
    assert result.exit_code == 0

def test_update_command_no_options(tmp_path, monkeypatch):
    monkeypatch.setattr("task_cli.storage.DATA_FILE", tmp_path / "tasks.json")
    runner = CliRunner()
    add_task("Buy groceries")
    result = runner.invoke(app, ["update", "1"])
    assert result.exit_code == 0
    assert "Description or status must be provided" in result.output

def test_update_command_status(tmp_path, monkeypatch):
    monkeypatch.setattr("task_cli.storage.DATA_FILE", tmp_path / "tasks.json")
    runner = CliRunner()
    add_task("Buy groceries")
    result = runner.invoke(app, ["update", "1", "--status", "done"])
    assert result.exit_code == 0

def test_update_command_invalid_status(tmp_path, monkeypatch):
    monkeypatch.setattr("task_cli.storage.DATA_FILE", tmp_path / "tasks.json")
    runner = CliRunner()
    add_task("Buy groceries")
    result = runner.invoke(app, ["update", "1", "--status", "invalid"])
    assert result.exit_code != 0

def test_update_non_existent_id_crashes(tmp_path, monkeypatch):
    monkeypatch.setattr("task_cli.storage.DATA_FILE", tmp_path / "tasks.json")
    runner = CliRunner()
    result = runner.invoke(app, ["update", "999", "--description", "Updated groceries"])
    assert result.exit_code != 0